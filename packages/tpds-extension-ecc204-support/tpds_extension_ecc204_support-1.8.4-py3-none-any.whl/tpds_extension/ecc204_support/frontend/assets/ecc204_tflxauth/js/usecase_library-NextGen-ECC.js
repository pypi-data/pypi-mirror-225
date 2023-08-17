ws = new WebSocket("ws://localhost:1302/websocket");

var UseCases = {
  // TFLEX Usecases list starts.....
  104: {
    title: "Asymmetric Authentication",
    selected: false,
    ids: [],
  },
  105: {
    title: "Symmetric Authentication",
    selected: false,
    ids: ["Slot3"],
  }
};

/* Display the TrustFLEX development boards */
$(document).ready(function () {
  for (var key in UseCases) {
    if (parseInt(key) < 200) {
      $('#hexGrid').append(
        $('<li>', { 'class': 'hex' }).append(
          $('<div>', { 'class': 'hexOut' }).append(
            $('<div>', { 'class': 'hexIn' }).append(
              $('<a>', { 'class': 'hexLink', 'id': key }).append(
                // $('<img>', {'src':UseCases[key].imgpath}),
                $('<p>', { 'text': UseCases[key].title }),
                $('<div>', { 'class': "onclick_usecase" }).append(
                  $('<img>', { 'src': "../images/check-mark-png-11553206004impjy81rdu.png" })
                ))))))
    }
  }
});


$(document).on("click", ".secure_provisioning_guide", function () {
  open_link("Documentation.html#" + $(this).attr('id'));
});

$(document).on("click", ".image_btn", function () {
  $(this).toggleClass('active');
  toggleUseCase($(this).attr('id'));
});

$(document).on("click", ".hexLink", function () {
  $(this).toggleClass('select');
  toggleUseCase($(this).attr('id'));
});

function clearSelectedUseCases(board) {
  for (var ele = 0; ele < Boards[board].usecases.length; ele++) {
    if (UseCases[Boards[board].usecases[ele]].selected === true) {
      toggleUseCase(Boards[board].usecases[ele]);
    }
  }
}

function toggleUseCase(useCase) {
  var useCaseName = UseCases[useCase].name;
  var item = document.getElementById(useCaseName + "Item");
  //var button = document.getElementById(useCaseName + "Btn");
  var img = document.getElementById(useCaseName + "Img")
  if (UseCases[useCase].selected === false) {
    var ids_l = UseCases[useCase].ids
    if (ids_l.includes("Slot1") == true) {
      document.getElementById("101").checked = false;
      document.getElementById("102").checked = true;
      cert1RadioHandler();
    }
    else {
      let checkbox101 = document.getElementById("101");
      let checkbox102 = document.getElementById("102")
      if (checkbox101)
        checkbox101.checked = true;

      if (checkbox102)
        checkbox102.checked = false;
    }
    UseCases[useCase].ids.forEach(element => {
      var rowElement = document.getElementById(element);
      rowElement.style['backgroundColor'] = 'LightSalmon'
    });
    UseCases[useCase].selected = true;
    /*button.style.backgroundColor = "#00bb00";
    button.innerHTML = "UNSELECT";
    button.classList.add("use_case_btn_selected");*/
  } else {
    var ids_l = UseCases[useCase].ids
    if (ids_l.includes("Slot1") == true) {
      document.getElementById("101").checked = true;
      document.getElementById("102").checked = false;
      cert1RadioHandler();
    }
    UseCases[useCase].ids.forEach(element => {
      var rowElement = document.getElementById(element);
      rowElement.style['backgroundColor'] = 'white';
    });
    UseCases[useCase].selected = false;
    /*button.style.backgroundColor = "#e40222";
    button.innerHTML = "SELECT";
    button.classList.remove("use_case_btn_selected");*/
  }
}

function validateUseCaseSlots() {
  //Object.keys(UseCases).length
  var usecaseElements;
  var alertUseCasesNames = "";
  var alertUseCaseSlots = "";
  var alertStatus = false;
  var radioName;

  for (usecaseElements in UseCases) {
    if (UseCases[usecaseElements].selected == true) {
      //console.log(UseCases[usecaseElements].ids);
      for (let i = 0; i < UseCases[usecaseElements].ids.length; i++) {
        var element = UseCases[usecaseElements].ids[i];
        if (element == "Slot1") {
          radioName = element.toLowerCase() + "certopt";
          if (getFormRadioValue(formNameMain, radioName) == "MCHPCert") {
            if (!alertUseCaseSlots.includes(element)) {
              alertUseCaseSlots += element + "\r\n";
              alertStatus = true;
            }
          }
        } else if (element == "custCertPubkey") {
          radioName = "slot4" + "dataopt";
          if (getFormRadioValue(formNameMain, radioName) == "unused") {
            alertUseCaseSlots += "CA Public key data" + "\r\n";
            alertStatus = true;
          }
        } else {
          radioName = element.toLowerCase() + "dataopt";
          if (getFormRadioValue(formNameMain, radioName) == "unused") {
            if (!alertUseCaseSlots.includes(element)) {
              alertUseCaseSlots += element + "\r\n";
              alertStatus = true;
            }
          }
        }
      }
    }
  }

  if (alertStatus) {
    alert("For the usecases selected, Data is required in the following slots: \r\n" + alertUseCaseSlots);
  }
  return alertStatus;
}
