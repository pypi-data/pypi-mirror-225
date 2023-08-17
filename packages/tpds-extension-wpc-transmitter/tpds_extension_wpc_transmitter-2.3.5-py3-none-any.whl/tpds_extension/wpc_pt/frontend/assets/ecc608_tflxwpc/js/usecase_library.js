var UseCases = {
  // TFLEX Usecases list starts.....
  100: {
      title: "Firmware Validation (Secure Boot)",
      selected: false,
      ids: ["Slot15"],
      allow_selection: true,
      default_selection: false
  },
  112: {
      title: " WPC Authentication",
      selected: false,
      ids: ["Slot3", "Slot4", "Slot5", "Slot9", "Slot13", "Slot14", "ptmcCodeId", "QiIdId", "CASequenceIdId"],
      prefix: 1,
      allow_selection: true,
      default_selection: true
  },
};

document
  .getElementById("prov_proto_tflxwpc")
  .addEventListener("click", provision_proto_fn);

function provision_proto_fn() {
  tflex_prov_proto(this.id);
}

$(document).ready(function () {
  for (var key in UseCases) {
    if (parseInt(key) < 200) {
      $("#hexGrid").append(
        $("<li>", { class: "hex" }).append(
          $("<div>", { class: "hexOut" }).append(
            $("<div>", { class: "hexIn" }).append(
              $("<a>", { class: "hexLink", id: key }).append(
                $("<p>", { text: UseCases[key].title }),
                $("<div>", { class: "onclick_usecase" }).append(
                  $("<img>", {
                    src: "../images/check-mark-png-11553206004impjy81rdu.png",
                  })
                )
              )
            )
          )
        )
      );
      if (UseCases[key].default_selection)
      {
          $('a#'+key+'.hexLink').trigger('click');
      }
    }
  }
});

$(document).on("click", ".secure_provisioning_guide", function () {
  open_link('Documentation.html#'+$(this).attr('id'))
});

$(document).on("click", ".image_btn", function () {
  $(this).toggleClass("active");
  toggleUseCase($(this).attr("id"));
});

$(document).on("click", ".hexLink", function () {
  if (UseCases[$(this).attr("id")].allow_selection === false) {
    alert("Currently, this Usecase selection is not supported.");
  } else {
    $(this).toggleClass("select");
    toggleUseCase($(this).attr("id"));
  }
});

function clearSelectedUseCases(board) {
  for (var ele = 0; ele < Boards[board].usecases.length; ele++) {
    if (UseCases[Boards[board].usecases[ele]].selected === true) {
      toggleUseCase(Boards[board].usecases[ele]);
    }
  }
}

function toggleUseCase(useCase) {
  if (UseCases[useCase].selected === false) {
    var ids_l = UseCases[useCase].ids;
    if (ids_l.includes("Slot10") == true) {
      if (UseCases[useCase].certs == "custom") {
        document.getElementById("1001").checked = false;
        document.getElementById("1002").checked = true;
        cert10RadioHandler();
      }
      if (UseCases[useCase].prefix == 2) {
        document.getElementById("cbid_devcertcn").checked = false;
        document.getElementById("cbid_devcertcn_pr").checked = true;
        document.getElementById("10certcommonname").disabled = false;
        document.getElementById("10certcommonname").value = "";
        document.getElementById("10certcommonname").placeholder =
          "Avnet IoTConnect Company ID";
      }
    } else {
      document.getElementById("1001").checked = true;
      document.getElementById("1002").checked = false;
      document.getElementById("cbid_devcertcn").checked = true;
      document.getElementById("cbid_devcertcn_pr").checked = false;
      document.getElementById("10certcommonname").disabled = true;
      document.getElementById("10certcommonname").value =
        "sn0123030405060708EE";
    }
    UseCases[useCase].ids.forEach((element) => {
      var rowElement = document.getElementById(element);
      rowElement.style["backgroundColor"] = "LightSalmon";
    });
    UseCases[useCase].selected = true;
    /*button.style.backgroundColor = "#00bb00";
        button.innerHTML = "UNSELECT";
        button.classList.add("use_case_btn_selected");*/
  } else {
    var ids_l = UseCases[useCase].ids;
    if (ids_l.includes("Slot10") == true) {
      if (UseCases[useCase].certs == "custom") {
        document.getElementById("1001").checked = true;
        document.getElementById("1002").checked = false;
        document.getElementById("cbid_devcertcn").checked = true;
        document.getElementById("cbid_devcertcn_pr").checked = false;
        document.getElementById("10certcommonname").disabled = true;
        document.getElementById("10certcommonname").value =
          "sn0123030405060708EE";
        cert10RadioHandler();
      }
    }
    UseCases[useCase].ids.forEach((element) => {
      var rowElement = document.getElementById(element);
      rowElement.style["backgroundColor"] = "white";
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
        if (element == "Slot10" || element == "Slot12") {
          radioName = element.toLowerCase() + "certopt";
          if (getFormRadioValue(formNameMain, radioName) == "MCHPCert") {
            if (!alertUseCaseSlots.includes(element)) {
              alertUseCaseSlots += element + "\r\n";
              alertStatus = true;
            }
          }
        } else if (element == "custCertPubkey") {
          radioName = "slot16" + "dataopt";
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
