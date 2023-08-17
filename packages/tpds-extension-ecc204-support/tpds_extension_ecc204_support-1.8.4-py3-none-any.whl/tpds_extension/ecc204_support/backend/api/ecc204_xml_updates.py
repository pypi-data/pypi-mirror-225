# -*- coding: utf-8 -*-
# 2019 to present - Copyright Microchip Technology Inc. and its subsidiaries.

# Subject to your compliance with these terms, you may use Microchip software
# and any derivatives exclusively with Microchip products. It is your
# responsibility to comply with third party license terms applicable to your
# use of third party software (including open source software) that may
# accompany Microchip software.

# THIS SOFTWARE IS SUPPLIED BY MICROCHIP "AS IS". NO WARRANTIES, WHETHER
# EXPRESS, IMPLIED OR STATUTORY, APPLY TO THIS SOFTWARE, INCLUDING ANY IMPLIED
# WARRANTIES OF NON-INFRINGEMENT, MERCHANTABILITY, AND FITNESS FOR A PARTICULAR
# PURPOSE. IN NO EVENT WILL MICROCHIP BE LIABLE FOR ANY INDIRECT, SPECIAL,
# PUNITIVE, INCIDENTAL OR CONSEQUENTIAL LOSS, DAMAGE, COST OR EXPENSE OF ANY
# KIND WHATSOEVER RELATED TO THE SOFTWARE, HOWEVER CAUSED, EVEN IF MICROCHIP
# HAS BEEN ADVISED OF THE POSSIBILITY OR THE DAMAGES ARE FORESEEABLE. TO THE
# FULLEST EXTENT ALLOWED BY LAW, MICROCHIP'S TOTAL LIABILITY ON ALL CLAIMS IN
# ANY WAY RELATED TO THIS SOFTWARE WILL NOT EXCEED THE AMOUNT OF FEES, IF ANY,
# THAT YOU HAVE PAID DIRECTLY TO MICROCHIP FOR THIS SOFTWARE.
from __future__ import annotations
import os
import json
from pathlib import Path
from lxml import etree
import datetime
from cryptography import x509
from tpds.certs.tflex_certs import TFLEXCerts
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from tpds.tp_utils.tp_keys import TPAsymmetricKey
from tpds.certs.cert_utils import get_device_public_key, get_backend, get_certificate_CN, get_certificate_issuer_CN

from wpc_pt_config.api.certs_schema import WPCRootCertParams
from wpc_pt_config.api.wpc_root import create_wpc_root_cert
from wpc_pt_config.api.wpc_mfg import create_wpc_mfg_cert
from wpc_pt_config.api.wpc_puc import create_wpc_puc_cert

from tpds.schema import get_ecc204_ta010_xsd_path
from tpds.schema.models.ecc204_1_1.ecc204_ta010_config_1_1 import (
    Ecc204Config, Ta010Config, DataSourceType, StaticBytesType, PublicBinaryDataType, SecretBinaryDataType,
    X509NameType, X509CertificateType, X509SignatureAlgorithmType, X509SignatureAlgorithmEcdsatype,
    X509CacertificateChainType, X509SerialNumberType, X509TimeType, X509SubjectPublicKeyInfoType,
    X520DirectoryStringOrFromSourceType, QiCertificateChainType, HashType, DataSourcesWriterType,
    DeviceGenerateKeyType, GenerateKeyEcctype, HsmrandomType, CounterType, BytesPadType, TemplateType,
    X509ExtensionsType, X509ExtensionType, DerbinaryDataOrFromSourceType
)


class ECC204_TA010_XMLUpdates():
    def __init__(self, base_xml) -> None:
        self.xml_path = os.path.join(os.path.dirname(
            __file__), "base", "ECC204_TA010_base.xml")
        self.xsd_path = get_ecc204_ta010_xsd_path()
        self.base_xml = base_xml
        xml_string = Path(self.xml_path).read_text()
        config = Ecc204Config if (
            base_xml in ['ECC204_TFLXAUTH', 'ECC204_TFLXWPC']) else Ta010Config
        self.xml_obj = XmlParser().from_string(xml_string, config)

    def save_root(self, dest_xml):
        config = SerializerConfig(pretty_print=True)
        serializer = XmlSerializer(config=config)
        Path(dest_xml).touch()
        with Path(dest_xml).open("w") as fp:
            serializer.write(out=fp, obj=self.xml_obj, ns_map={
                None: "https://www.microchip.com/schema/ECC204_TA010_Config_1.1"})

        status = self.__validate_xml(dest_xml, self.xsd_path)
        if (status != "valid"):
            Path(dest_xml).unlink(missing_ok=True)
            raise BaseException(f"XML generation failed with: {status}")

    def process_cert_xml(self, cert_data):
        '''
        process X509 certificate data for provisioning XML
        '''
        # To Resolve ForwardRef Problem
        X509CertificateType.TbsCertificate.__pydantic_model__.update_forward_refs()
        X509NameType.RelativeDistinguishedName.__pydantic_model__.update_forward_refs()

        ds = DataSourceType(name=cert_data.get("name"),
                            description=cert_data.get("desc"))
        ds.x509_certificate = X509CertificateType()
        ds.x509_certificate.ca_certificate_chain = X509CacertificateChainType(
            value=cert_data.get("cert_chain"))
        ds.x509_certificate.signature_algorithm = X509SignatureAlgorithmType(
            ecdsa=X509SignatureAlgorithmEcdsatype(hash=cert_data.get("hash")))
        ds.x509_certificate.tbs_certificate = X509CertificateType.TbsCertificate(
            version="V3")
        ds.x509_certificate.tbs_certificate.serial_number = X509SerialNumberType(
            value=cert_data.get("serial_number"))
        ds.x509_certificate.tbs_certificate.validity = X509CertificateType.TbsCertificate.Validity()
        ds.x509_certificate.tbs_certificate.validity.not_before = X509TimeType(
            value=cert_data.get("not_valid_before"), type="Auto", from_source="True")
        ds.x509_certificate.tbs_certificate.validity.not_after = X509TimeType(
            value=cert_data.get("not_valid_after"), type="Auto", from_source="False")
        if cert_data.get("cert_common_name") and cert_data.get("cert_common_name") != "":
            ds.x509_certificate.tbs_certificate.subject = X509NameType(relative_distinguished_name=[X509NameType.RelativeDistinguishedName(
                common_name=X520DirectoryStringOrFromSourceType(type="UTF8_String", from_source="False", encoding="String_UTF8", value=cert_data.get("cert_common_name")))])
        subject_public_key = "__dummy_value__"
        if cert_data.get("subject_public_key_info"):
            subject_public_key = cert_data.get("subject_public_key_info")
        ds.x509_certificate.tbs_certificate.subject_public_key_info = X509SubjectPublicKeyInfoType(
            key=X509SubjectPublicKeyInfoType.Key(value=subject_public_key))
        if cert_data.get("extension"):
            extension_params = cert_data.get("extension")
            ds.x509_certificate.tbs_certificate.extensions = X509ExtensionsType(extension=[X509ExtensionType(
                extn_id=extension_params.get("extn_id"), critical=extension_params.get("critical"), extn_value=DerbinaryDataOrFromSourceType(value=extension_params.get("extn_value"), from_source=extension_params.get("from_source")))])
        return ds

    def __validate_xml(self, xml_path: str, xsd_path: str):
        '''
        checks xml against it's xsd file
        '''
        with open(xsd_path) as f_schema:
            schema_doc = etree.parse(f_schema)
            schema = etree.XMLSchema(schema_doc)
            parser = etree.XMLParser(schema=schema)

            with open(xml_path) as f_source:
                try:
                    etree.parse(f_source, parser)
                except etree.XMLSyntaxError as e:
                    return e
        return "valid"


class ECC204_TA010_TFLXAUTH_XMLUpdates(ECC204_TA010_XMLUpdates):
    def update_with_user_data(self, user_data):
        user_data = json.loads(user_data)
        self.__process_slot_config(user_data)
        self.__process_slot_data(user_data)

    def __process_slot_config(self, user_data):
        '''
        process config slots to provisiong XML
        '''
        self.xml_obj.config_name = f"{self.base_xml} {user_data.get('xml_type')}"

        # configuration_subzone_0
        configuration_subzone_0 = self.xml_obj.configuration_subzone_0
        configuration_subzone_0.io_options.interface = "SWI_PWM" if (
            user_data.get("interface") == "swi") else "I2C"
        if user_data.get("sn01"):
            configuration_subzone_0.sn_0_1.value = user_data.get("sn01")
        if user_data.get("sn8"):
            configuration_subzone_0.sn_8.value = user_data.get("sn8")

        # configuration_subzone_1
        configuration_subzone_1 = self.xml_obj.configuration_subzone_1
        configuration_subzone_1.chip_mode.cmos_en = "Fixed_Reference" if user_data.get(
            "fixed_reference") else "VCC_Referenced"
        configuration_subzone_1.chip_mode.clock_divider = "0b11"
        configuration_subzone_1.chip_mode.rng_nrbg_health_test_auto_clear = "True" if user_data.get(
            "health_test") else "False"
        configuration_subzone_1.slot_config0.limited_use = "True" if (
            user_data.get("limited_key_use") == "private") else "False"
        configuration_subzone_1.slot_config3.limited_use = "True" if (
            user_data.get("limited_key_use") == "secret") else "False"
        configuration_subzone_1.slot_config3.write_mode = "Encrypted" if user_data.get(
            "encrypt_write") else "Clear"
        configuration_subzone_1.lock = "True"

        # configuration_subzone_2
        configuration_subzone_2 = self.xml_obj.configuration_subzone_2
        configuration_subzone_2.counts_remaining = 10000 - \
            user_data.get("counter_value")
        configuration_subzone_2.lock = "True"

        # configuration_subzone_3
        configuration_subzone_3 = self.xml_obj.configuration_subzone_3
        configuration_subzone_3.device_address = f'0x{user_data.get("device_address")}'
        configuration_subzone_3.cmp_mode = "True" if user_data.get(
            "compliance") else "False"
        configuration_subzone_3.lock = "True"

    def __process_slot_data(self, user_data):
        '''
        Process data slots to provisioning XML
        '''
        slot_info = user_data.get("slot_info")

        # slot locks
        slot_locks = self.xml_obj.slot_locks
        slot_locks.slot_0 = "True"
        slot_locks.slot_1 = "True" if (slot_info[1].get(
            "slot_lock") == "enabled") else "False"
        slot_locks.slot_2 = "True" if (slot_info[2].get(
            "slot_lock") == "enabled") else "False"
        slot_locks.slot_3 = "True" if (slot_info[3].get(
            "slot_lock") == "enabled") else "False"

        self.xml_obj.data_sources.data_source = []

        # Slot 0 - Data_Sources - Device_Generate_Key
        ds = DataSourceType(name="Device_Public_Key")
        ds.device_generate_key = DeviceGenerateKeyType(target="Slot 0")
        ds.device_generate_key.ecc = GenerateKeyEcctype(curve="secp256r1")
        self.xml_obj.data_sources.data_source.append(ds)

        # Slot 1 - Data_Sources - certs
        cert_data = user_data.get('slot_info')[1]
        if (cert_data.get('cert_type') == "custCert"):
            self.__process_certs(cert_data)

        # Slot 2 - Data_Sources - general
        if (slot_info[2].get("data")):
            ds = DataSourceType(name="Slot_2_Client_Data",
                                description="Slot 2 general public data storage (64 bytes)")
            ds.static_bytes = StaticBytesType(public=PublicBinaryDataType(
                value=slot_info[2].get("data"), encoding="Hex"))
            self.xml_obj.data_sources.data_source.append(ds)

        # Slot 3 - Data_Sources - secret
        if (slot_info[3].get("data")):
            ds = DataSourceType(name="Slot_3_Client_Data",
                                description="Slot 3 Storage for a secret key")
            ds.static_bytes = StaticBytesType(secret=SecretBinaryDataType(
                encoding="Hex", key_name="HMAC_Secret_key", algorithm="AES256_GCM"))
            ds.static_bytes.secret.encrypted = "False"
            ds.static_bytes.secret.value = slot_info[3].get("data")
            self.xml_obj.data_sources.data_source.append(ds)

        # data source writer
        self.xml_obj.data_sources.writer = []

        # Writer For Slot 2
        if (slot_info[2].get("data")):
            wr = DataSourcesWriterType(
                source_name="Slot_2_Client_Data", target="Slot 2")
            self.xml_obj.data_sources.writer.append(wr)

        # Writer For Slot 3
        if (slot_info[3].get("data")):
            wr = DataSourcesWriterType(
                source_name="Slot_3_Client_Data", target="Slot 3")
            self.xml_obj.data_sources.writer.append(wr)

        # data source wrapped key
        self.xml_obj.data_sources.wrapped_key = []

    def __process_certs(self, cert_data):
        tflex_certs = TFLEXCerts()
        tflex_certs.build_root(
            org_name=cert_data.get('signer_ca_org'),
            common_name=cert_data.get('signer_ca_cn'),
            validity=int(cert_data.get('s_cert_expiry_years')),
            user_pub_key=bytes(cert_data.get('signer_ca_pubkey'), 'ascii'))
        tflex_certs.build_signer_csr(
            org_name=cert_data.get('s_cert_org'),
            common_name=cert_data.get('s_cert_cn'),
            signer_id='FFFF')
        tflex_certs.build_signer(
            validity=int(cert_data.get('s_cert_expiry_years')))
        tflex_certs.build_device(
            device_sn=cert_data.get('d_cert_cn'),
            org_name=cert_data.get('d_cert_org'),
            validity=int(cert_data.get('d_cert_expiry_years')))

        signer_pem = tflex_certs.signer.get_certificate_in_pem()
        root_pem = tflex_certs.root.get_certificate_in_pem()
        cert_chain_text = f'\nSubject: CN={cert_data.get("s_cert_cn")},O={cert_data.get("s_cert_org")}\n' + \
            f'Issuer: CN={cert_data.get("signer_ca_cn")},O={cert_data.get("signer_ca_org")}\n' + \
            str(signer_pem, 'utf-8') + \
            f'\n\nSubject: CN={cert_data.get("signer_ca_cn")},O={cert_data.get("signer_ca_org")}\n' + \
            f'Issuer: {cert_data.get("signer_ca_cn")},O={cert_data.get("signer_ca_org")}\n' + \
            str(root_pem, 'utf-8')\

        device_cert = x509.load_pem_x509_certificate(
            tflex_certs.device.get_certificate_in_pem())
        current_date = datetime.datetime.now()
        expiry_date = current_date.replace(
            year=current_date.year + int(cert_data.get("d_cert_expiry_years")))

        cert_data = {
            "name": "Slot_1_Client_Data",
            "desc": "Slot 1 Device and Signer compressed certificate",
            "cert_chain": cert_chain_text,
            "hash": "SHA256",
            "version": "V3",
            "serial_number": f'sn{device_cert.serial_number}',
            "not_valid_before": current_date.strftime("Z%Y%m%d"),
            "not_valid_after": expiry_date.strftime("Z%Y%m%d"),
            "cert_common_name": ""
        }

        ds = self.process_cert_xml(cert_data=cert_data)
        self.xml_obj.data_sources.data_source.append(ds)


class ECC204_TA010_TFLXWPC_XMLUpdates(ECC204_TA010_XMLUpdates):
    def update_with_user_data(self, user_data):
        user_data = json.loads(user_data)
        self.__process_slot_config(user_data)
        self.__process_slot_data(user_data)

    def __process_slot_config(self, user_data):
        self.xml_obj.config_name = f"{self.base_xml} {user_data.get('xml_type')}"

        # configuration_subzone_0
        configuration_subzone_0 = self.xml_obj.configuration_subzone_0
        configuration_subzone_0.io_options.interface = "I2C"
        if user_data.get("sn01"):
            configuration_subzone_0.sn_0_1.value = user_data.get("sn01")
        if user_data.get("sn8"):
            configuration_subzone_0.sn_8.value = user_data.get("sn8")

        # configuration_subzone_1
        configuration_subzone_1 = self.xml_obj.configuration_subzone_1
        configuration_subzone_1.chip_mode.cmos_en = "Fixed_Reference" if user_data.get(
            "fixed_reference") else "VCC_Referenced"
        configuration_subzone_1.chip_mode.clock_divider = "0b11"
        configuration_subzone_1.slot_config3.limited_use = "True" if (
            user_data.get("limited_key_use") == "HMAC") else "False"
        configuration_subzone_1.slot_config3.write_mode = "Encrypted" if user_data.get(
            "encrypt_write") else "Clear"
        configuration_subzone_1.lock = "True"

        # configuration_subzone_2
        configuration_subzone_2 = self.xml_obj.configuration_subzone_2
        configuration_subzone_2.counts_remaining = 10000 - \
            user_data.get("counter_value")
        configuration_subzone_2.lock = "True"

        # configuration_subzone_3
        configuration_subzone_3 = self.xml_obj.configuration_subzone_3
        configuration_subzone_3.device_address = f'0x{user_data.get("device_address")}'
        configuration_subzone_3.lock = "True"

    def __process_slot_data(self, user_data):
        slot_info = user_data.get("slot_info")

        # slot locks
        slot_locks = self.xml_obj.slot_locks
        slot_locks.slot_0 = "True"
        slot_locks.slot_1 = "True" if (slot_info[1].get(
            "slot_lock") == "enabled") else "False"
        slot_locks.slot_2 = "True" if (slot_info[2].get(
            "slot_lock") == "enabled") else "False"
        slot_locks.slot_3 = "True" if (slot_info[3].get(
            "slot_lock") == "enabled") else "False"

        self.xml_obj.data_sources.data_source = []

        # data source - Device generate key
        device_gkey_ds = DataSourceType(name="Device_Public_Key")
        device_gkey_ds.device_generate_key = DeviceGenerateKeyType(
            ecc=GenerateKeyEcctype(curve="secp256r1"), target="Slot 0")
        self.xml_obj.data_sources.data_source.append(device_gkey_ds)

        # data source - hsm random
        hsm_rand_ds = DataSourceType(name="Certificate_SN_Raw")
        hsm_rand_ds.hsm_random = HsmrandomType(size=9, secret_data="False")
        self.xml_obj.data_sources.data_source.append(hsm_rand_ds)

        # data source - Force Non-negative fixed size
        force_nnfs_ds = DataSourceType(name="Certificate_SN")
        force_nnfs_ds.force_nonnegative_fixed_size = DataSourceType.ForceNonnegativeFixedSize(
            input="Certificate_SN_Raw")
        self.xml_obj.data_sources.data_source.append(force_nnfs_ds)

        # data source - current_date_time
        cdt_ds = DataSourceType(name="Certificate_Not_Before")
        cdt_ds.current_date_time = ""
        self.xml_obj.data_sources.data_source.append(cdt_ds)

        # data source - counter
        counter_ds = DataSourceType(name="RSID_Counter")
        counter_ds.counter = CounterType(counter_name="RSID Counter " + user_data.get(
            "ptmc") + "-" + user_data.get("ca_seq_id"), size=9, byte_order="Big", signed="False")
        self.xml_obj.data_sources.data_source.append(counter_ds)

        # data source WPC_Qi_Auth_RSID_Extn_Value
        rsid_extn_ds = DataSourceType(name="WPC_Qi_Auth_RSID_Extn_Value",
                                      description="Composes the wpc-qiAuth-rsid (2.23.148.1.2) extension value manually. It's an ASN.1 octet string (tag 04) with a fixed size of 9 bytes.")
        rsid_extn_ds.template = TemplateType(definition=TemplateType.Definition(
            value="04 09 {RSID_Counter}", encoding="Hex"))
        self.xml_obj.data_sources.data_source.append(rsid_extn_ds)

        # Slot 1 - Data_Sources - Full product unit certificate
        self.__process_wpc_certs_data(user_data)

        # data source - bytes pad qi_product_unit_certificate
        qi_puc_bytespad_ds = DataSourceType(name="Qi_Product_Unit_Certificate_Padded")
        qi_puc_bytespad_ds.bytes_pad = BytesPadType(input="Qi_Product_Unit_Certificate.Certificate", fixed_size=BytesPadType.FixedSize(
            output_size=320, pad_byte="0x00", alignment="Pad_Right"))
        self.xml_obj.data_sources.data_source.append(qi_puc_bytespad_ds)

        # data source certificate chain
        qi_chain_ds = DataSourceType(name="Qi_Certificate_Chain")
        qi_chain_ds.qi_certificate_chain = QiCertificateChainType(root_ca_certificate="Qi_Product_Unit_Certificate.CA_Certificate_2",
                                                                  manufacturer_ca_certificate="Qi_Product_Unit_Certificate.CA_Certificate_1", product_unit_certificate="Qi_Product_Unit_Certificate.Certificate")
        self.xml_obj.data_sources.data_source.append(qi_chain_ds)

        # data source chain digest
        qi_chain_digest = DataSourceType(name="Qi_Certificate_Chain_Digest")
        qi_chain_digest.hash = HashType(
            input="Qi_Certificate_Chain", algorithm="SHA256")
        self.xml_obj.data_sources.data_source.append(qi_chain_digest)

        # data source - bytes pad qi certificate chain digest
        qi_ccd_bytespad_ds = DataSourceType(name="Qi_Certificate_Chain_Digest_Padded")
        qi_ccd_bytespad_ds.bytes_pad = BytesPadType(input="Qi_Certificate_Chain_Digest", fixed_size=BytesPadType.FixedSize(
            output_size=64, pad_byte="0x00", alignment="Pad_Right"))
        self.xml_obj.data_sources.data_source.append(qi_ccd_bytespad_ds)

        # Slot 3 - Data_Sources - secret
        if (slot_info[3].get("data")):
            ds = DataSourceType(name="Slot_3_Client_Data",
                                description="Slot 3 Storage for a secret key")
            ds.static_bytes = StaticBytesType(secret=SecretBinaryDataType(
                encoding="Hex", key_name="HMAC_Secret_key", algorithm="AES256_GCM"))
            ds.static_bytes.secret.encrypted = "False"
            ds.static_bytes.secret.value = slot_info[3].get("data")
            self.xml_obj.data_sources.data_source.append(ds)

        # data source writer
        self.xml_obj.data_sources.writer = []
        self.xml_obj.data_sources.writer.append(
            DataSourcesWriterType(source_name="Qi_Product_Unit_Certificate_Padded", target="Slot 1"))
        self.xml_obj.data_sources.writer.append(DataSourcesWriterType(
            source_name="Qi_Certificate_Chain_Digest_Padded", target="Slot 2"))
        if (slot_info[3].get("data")):
            self.xml_obj.data_sources.writer.append(DataSourcesWriterType(
            source_name="Slot_3_Client_Data", target="Slot 3"))

        # data source wrapped key
        self.xml_obj.data_sources.wrapped_key = []

    def __process_wpc_certs_data(self, user_data):
        root_key = None
        mfg_key = None
        ptmc_code = user_data.get('ptmc')
        ca_seq_id = user_data.get('ca_seq_id')
        qi_id = user_data.get('qi_id')
        puc_pubkey = get_device_public_key(None)
        puc_pubkey = ec.EllipticCurvePublicNumbers(
            x=int(puc_pubkey[:64], 16),
            y=int(puc_pubkey[64:], 16),
            curve=ec.SECP256R1()).public_key(get_backend())

        # Generate root certificate
        root_key = TPAsymmetricKey(key=root_key)
        root_key.get_private_pem()
        root_params = WPCRootCertParams(ca_key=root_key.get_private_pem())
        wpc_root_crt = create_wpc_root_cert(
            root_key.get_private_key(),
            root_params.root_cn,
            root_params.root_sn)

        # Generate Manufacturer certificate
        mfg_key = TPAsymmetricKey(key=mfg_key)
        mfg_key.get_private_pem()
        wpc_mfg_crt = create_wpc_mfg_cert(
            int(ptmc_code, 16),
            int(ca_seq_id, 16),
            int(qi_id),
            mfg_key.get_public_key(),
            root_key.get_private_key(),
            wpc_root_crt)

        # Generate Product Unit certificate
        wpc_puc_crt = create_wpc_puc_cert(
            qi_id=int(qi_id),
            rsid=int.from_bytes(os.urandom(4), byteorder='big'),
            public_key=puc_pubkey,
            ca_private_key=mfg_key.private_key,
            ca_certificate=wpc_mfg_crt)

        puc_key = TPAsymmetricKey()
        puc_key.set_public_key(puc_pubkey)

        cert_chain_text = f'\nSubject: CN={get_certificate_CN(wpc_mfg_crt)}\n' + \
            f'Issuer: CN={get_certificate_issuer_CN(wpc_mfg_crt)}\n' + \
            str(wpc_root_crt.public_bytes(
                encoding=serialization.Encoding.PEM), 'utf-8') + \
            f'\n\nSubject: CN={get_certificate_CN(wpc_root_crt)}\n' + \
            f'Issuer: CN={get_certificate_issuer_CN(wpc_root_crt)}\n' + \
            str(wpc_mfg_crt.public_bytes(
                encoding=serialization.Encoding.PEM), 'utf-8')\

        cert_data = {
            "name": "Qi_Product_Unit_Certificate",
            "desc": "Product Unit Full Certificate",
            "cert_chain": cert_chain_text,
            "hash": "SHA256",
            "version": "V3",
            "serial_number": "Certificate_SN",
            "not_valid_before": "Certificate_Not_Before",
            "not_valid_after": "9999-12-31T23:59:59",
            "cert_common_name": get_certificate_CN(wpc_puc_crt),
            "subject_public_key_info": "Device_Public_Key",
            "extension": {
                "extn_id": "2.23.148.1.2",
                "critical": "True",
                "from_source": "True",
                "extn_value": "WPC_Qi_Auth_RSID_Extn_Value"
            }
        }
        ds = self.process_cert_xml(cert_data=cert_data)
        self.xml_obj.data_sources.data_source.append(ds)


if __name__ == "__main__":
    pass
