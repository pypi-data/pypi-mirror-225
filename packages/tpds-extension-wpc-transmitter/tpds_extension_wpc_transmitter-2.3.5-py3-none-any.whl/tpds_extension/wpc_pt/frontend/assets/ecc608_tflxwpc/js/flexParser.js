var formNameMain = slotdataform;

var keyLoadConfig = {
    0: "noLoad",
    1: "noLoad",
    2: "noLoad",
    3: "noLoad",
    4: "noLoad",
    5: "noLoad",
    6: "load",
    7: "noLoad",
    8: "noLoad",
    9: "noLoad",
    10: "noLoad",
    11: "noLoad",
    12: "noLoad",
    13: "noLoad",
    14: "noLoad",
    15: "load"
};

var slotsize = {
    0: "32",
    1: "32",
    2: "32",
    3: "32",
    4: "32",
    5: "32",
    6: "32",
    7: "32",
    8: "416",
    9: "64",
    10: "64",
    11: "64",
    12: "64",
    13: "64",
    14: "64",
    15: "64",
    16: "64"
}

var tflexSlotType = {
    0: "private",
    1: "private",
    2: "private",
    3: "general",
    4: "general",
    5: "general",
    6: "secret",
    7: "general",
    8: "general",
    9: "general",
    10: "cert",
    11: "cert",
    12: "cert",
    13: "general",
    14: "general",
    15: "public"
}

var slotValidateDict = {
    0: "none",
    1: "none",
    2: "none",
    3: "none",
    4: "none",
    5: "none",
    6: "none",
    7: "none",
    8: "none",
    9: "none",
    10: "none",
    11: "none",
    12: "none",
    13: "none",
    14: "none",
    15: "none",
    16: "none"
};

function validateSlotOpt(){
    for(var i=0; i<16; i++){
        if(slotValidateDict[i] == "invalid"){
            alert("Enter valid data in slot " + i);
            return false;
        }
    }
    return true;
}

function verify_slot_data_bytes(slot_data, slot_number){
    var formatedString = slot_data.replaceAll(" ", "").replaceAll("\n", "").replaceAll("\r", "").replaceAll("\t", "").replaceAll("0x", "").replaceAll(",", "").toUpperCase();
    var slotDataValid = false;

    if ((slotsize[slot_number] * 2) == formatedString.length) {
        if (is_hex(formatedString)) {
            var string = "Data valid,"
            string += " entered values are:\n"
            string += prettyPrintHex(formatedString, 32);
            slotDataValid = true;
        } else {
            alert("Error: Data contains non-hex characters");
            slotDataValid = false;
        }
    } else {
        if (slot_number != 16)
            alert("The slot"+slot_number+"expects: " + slotsize[slot_number] + "bytes" + "\nYou have entered: " + (formatedString.length / 2) + "bytes");
        else
            alert("The custom root expects: " + slotsize[slot_number] + "bytes" + "\nYou have entered: " + (formatedString.length / 2) + "bytes");
        slotDataValid = false;
    }
    return slotDataValid;
}

function get_clean_slot_data_bytes(slot_data){
    return slot_data.replaceAll(" ", "").replaceAll("\n", "").replaceAll("\r", "").replaceAll("\t", "").replaceAll("0x", "").replaceAll(",", "").toUpperCase()
}

function gererateXML(xml_type) {
    var secretSlots = [6];
    var XMLContainsSecrets = false;

    let jsObj = {'base_xml': 'ECC608A-MAH-TFLXWPC.xml'}
    Object.assign(jsObj, {['xml_type']: xml_type});
    devIface = getFormRadioValue(formNameMain, "devIface")
    Object.assign(jsObj, {['interface']: devIface});
    otp_data = devIface == 'i2c' ? '601B1E853B13C775' : 'FFFFFFFFFFFFFFFF'

    // Update the slots with user's data.
    var jsSlotsData = []
    for (var i = 0; i < 16; i++) {
        let jsSlot = {'slot_id': i}
        Object.assign(jsSlot, {['slot_type']: tflexSlotType[i]});
        Object.assign(jsSlot, {['key_load_config']: keyLoadConfig[i]});
        var slotLock = document.getElementById("slotlock" + i.toString())
        var slot_lock_data =  slotLock != null ? slotLock.checked ? 'enabled':'disabled' : null
        Object.assign(jsSlot, {['slot_lock']: slot_lock_data});

        if (keyLoadConfig[i] == "load")
        {
            slot_data_bytes = getFormDataSlot(formNameMain, i)
            if (slot_data_bytes != null){
                if(verify_slot_data_bytes(slot_data_bytes, i)){
                    slot_data_bytes = get_clean_slot_data_bytes(slot_data_bytes)
                    slotValidateDict[i] = "valid"
                }
                else{
                    return
                }
            }
        }

        if (keyLoadConfig[i] == "noLoad") {
        }
        else if (keyLoadConfig[i] == "load") {
            Object.assign(jsSlot, {['data']: slot_data_bytes});
        }
        else if (keyLoadConfig[i] == "cert"){
            var radioName = "slot" + i + "certopt";
            // Getting value from selection button
            var certOptValue = getFormRadioValue(formNameMain, radioName);
            if (certOptValue == 'custCert')
            {
                if((document.getElementById(i + "certname").value == '') ||
                    (document.getElementById(i + "certcommonname").value == '') ||
                    (document.getElementById(i + "certyear").value == ''))
                {
                    alert("For Custom Certificates, all certificate fields to be populated!. Please verify fields in Slot"+i+".")
                    return
                }
                else if (i == 12)
                {
                    if((document.getElementById("16certname").value == '') ||
                    (document.getElementById("16certcommonname").value == ''))
                    {
                        alert("For Custom Certificates, all certificate fields to be populated!. Please verify Custom root Information.")
                        return
                    }

                    slot16_data_bytes = getFormDataSlot(formNameMain, 16)
                    if (slot16_data_bytes == null){
                        alert('Custom root public key data is not complete... Please check and try again.')
                        return
                    }
                    else{
                        if(verify_slot_data_bytes(slot16_data_bytes, 16))
                            slot16_data_bytes = get_clean_slot_data_bytes(slot16_data_bytes)
                        else
                            return
                    }
                }
            }

            Object.assign(jsSlot, {['cert_type']: certOptValue});

            if(certOptValue == "custCert"){
                Object.assign(jsSlot, {['cert_org']: document.getElementById(i + "certname").value});
                Object.assign(jsSlot, {['cert_cn']: 'sn0123030405060708EE'});
                if((i==10) && is_custom_pr_selected())
                    Object.assign(jsSlot, {['cert_cn']: document.getElementById(i + "certcommonname").value + '-0123030405060708EE'});
                else
                    Object.assign(jsSlot, {['cert_cn']: document.getElementById(i + "certcommonname").value});
                if(i==12)
                    Object.assign(jsSlot, {['cert_cn']: document.getElementById(i + "certcommonname").value});
                Object.assign(jsSlot, {['cert_expiry_years']: document.getElementById(i + "certyear").value});
                if (i ==12)
                {
                    Object.assign(jsSlot, {['signer_ca_org']: document.getElementById("16certname").value});
                    Object.assign(jsSlot, {['signer_ca_cn']: document.getElementById("16certcommonname").value});
                    Object.assign(jsSlot, {['signer_ca_pubkey']: slot16_data_bytes});
                }
            }
        }
        else {
            console.error("Config Error");
        }

        // Code to change mode secret slots to random if not used
        if(secretSlots.includes(i)){
            if(null != (status = getFormRadioValue(formNameMain, "slot" + i + "dataopt"))){
                if(status != "unused"){
                    XMLContainsSecrets = true;
                }
            }
        }
        jsSlotsData.push(jsSlot)
    }

    Object.assign(jsObj, {['slot_info']: jsSlotsData});
    Object.assign(jsObj, {['sboot_latch']: getFormRadioValue(formNameMain, "sbootLatchName")});

    manIdHexString = document.getElementById("manIdHexId").value;
    if(manIdHexString == "")
        manIdHexString = "01"
    Object.assign(jsObj, {['man_id']: manIdHexString});

    partNumberString = document.getElementById("partNumberId").value.toUpperCase();
    if(partNumberString == "")
        partNumberString = "ECC608-MAHAA-T"
    Object.assign(jsObj, {['part_number']: partNumberString});
    Object.assign(jsObj, {['otp_zone']: otp_data.padEnd(128, '0')});

    ptmcString = document.getElementById("ptmcCodeId").value.toUpperCase();
    qiIdString = document.getElementById("QiIdId").value.toUpperCase();
    caSeqIdString = document.getElementById("CASequenceIdId").value.toUpperCase();

    if(xml_type == 'proto_xml')
    {
        ptmcString = ptmcString == "" ? "004E" : ptmcString
        qiIdString = qiIdString == "" ? "11430" : qiIdString
        caSeqIdString = caSeqIdString == "" ? "01" : caSeqIdString
    }
    if((ptmcString == "") || (qiIdString == "") || (caSeqIdString == ""))
    {
        alert("All WPC fields MUST be populated.")
        return;
    }
    Object.assign(jsObj, {['ptmc']: ptmcString});
    Object.assign(jsObj, {['qi_id']: qiIdString});
    Object.assign(jsObj, {['ca_seq_id']: caSeqIdString});

    var useCaseValid = validateUseCaseSlots();
    var slotDataValidity = validateSlotOpt();

    if (useCaseValid == false && slotDataValidity == true) {
        if(XMLContainsSecrets){
            // alert("Secrets in the generated XML output file are not encrypted. \n\nThe file needs to be encrypted before it can be sent over to Microchip provisioning service.");
        }
        // console.log(JSON.stringify(jsObj));
        json_obj(JSON.stringify(jsObj));
    }
}

function setRadioValue(form, radioName, radioSelect){
    var radios = form.elements[radioName];

    for (var i = 0; i < radios.length; i++){
        if (radios[i].value == radioSelect){
            radios[i].checked = true;
        }
        else{
            radios[i].checked = false;
        }
    }

    return null;
}

function getFormRadioValue(form, name){
    var radios = form.elements[name];
    if (radios === undefined){
        return null;
    }
    for (var i = 0; i < radios.length; i++){
        if (radios[i].checked == true){
            return radios[i].value;
        }
    }

    return null;
}

function getFormDataSlot(form, slotNumber){
    var radioName = "slot" + slotNumber + "dataopt";
    var status;
    var slotData = null;

    if(null != (status = getFormRadioValue(form, radioName))){
        if(status == "unused"){
            slotData = null;
        }
        else if(status == "hexdata"){
            slotData = document.getElementById(radioName + "id").value;
        }
        else if(status == "pemdata"){
            slotData = document.getElementById(radioName + "id").value;
        }
        else{
            console.error("Unknown radio value");
            slotData = null;
        }
    }
    else{
        console.error("Radio Value fetch error")
    }
    return slotData;
}

function getDataFromSlot(radioName){
    var status;
    var slotData = null;

    if(null != (status = getFormRadioValue(formNameMain, radioName))){
        if(status == "unused"){
            //Do nothing?
            slotData = null;
        }
        else if(status == "hexdata"){
            slotData = document.getElementById(radioName + "id").value;
        }
        else if(status == "pemdata"){
            slotData = null;
        }
        else{
            console.error("Unknown radio value");
            slotData = null;
        }
    }
    else{
        console.error("Radio Value fetch error")
    }
    return slotData;
}

String.prototype.replaceAll = function(search, replacement) {
    var target = this;
    return target.replace(new RegExp(search, 'g'), replacement);
};