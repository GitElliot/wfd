Students = new Meteor.Collection('students');
Words = new Meteor.Collection('words');
Campaigns = new Meteor.Collection('campaigns');



if (Meteor.isClient) {
  
  Session.setDefault('appName', "Aztec's Teach by Text&trade; Platform");
  Session.setDefault('showStudentDialog', false);
  Session.setDefault('editing_student',  false);
  Session.setDefault('editing_word', false);
  Session.setDefault('editing_campaign', false);
  
  Session.setDefault('studentCursor', 0);
  Session.setDefault('wordCursor', 0);
  Session.setDefault('campaignCursor', 0);
  
  
  Meteor.Router.add({
    '/':'homepage',
    '/students':'students',
    '/wordgroups':'wordgroups',
    '/campaigns':'campaigns'
  })
  
  Meteor.autorun(function() {
    Meteor.subscribe("students", Session.get('studentCursor'));
    Meteor.subscribe("words", Session.get('wordCursor'));
    Meteor.subscribe("campaigns", Session.get('campaignCursor'));    
    
  })    
    
  
  Template.menu.appName = function(){
    return Session.get('appName');
  }
  
  //JAVASCRIPT FOR homepage        JAVASCRIPT FOR homepage         JAVASCRIPT FOR homepage    JAVASCRIPT FOR homepage  
  //JAVASCRIPT FOR homepage        JAVASCRIPT FOR homepage         JAVASCRIPT FOR homepage    JAVASCRIPT FOR homepage
  //JAVASCRIPT FOR homepage        JAVASCRIPT FOR homepage         JAVASCRIPT FOR homepage    JAVASCRIPT FOR homepage
  //JAVASCRIPT FOR homepage        JAVASCRIPT FOR homepage         JAVASCRIPT FOR homepage    JAVASCRIPT FOR homepage
  //JAVASCRIPT FOR homepage        JAVASCRIPT FOR homepage         JAVASCRIPT FOR homepage    JAVASCRIPT FOR homepage
  
  Accounts.ui.config({
    passwordSignupFields: 'USERNAME_ONLY'
  });
  

//  Accounts.onLogin(function(options, user) {
//    alert("login now");
//  });
  
  
  
  
  //JAVASCRIPT FOR STUDENTS        JAVASCRIPT FOR STUDENTS         JAVASCRIPT FOR STUDENTS    JAVASCRIPT FOR STUDENTS
  //JAVASCRIPT FOR STUDENTS        JAVASCRIPT FOR STUDENTS         JAVASCRIPT FOR STUDENTS    JAVASCRIPT FOR STUDENTS
  //JAVASCRIPT FOR STUDENTS        JAVASCRIPT FOR STUDENTS         JAVASCRIPT FOR STUDENTS    JAVASCRIPT FOR STUDENTS
  //JAVASCRIPT FOR STUDENTS        JAVASCRIPT FOR STUDENTS         JAVASCRIPT FOR STUDENTS    JAVASCRIPT FOR STUDENTS
  //JAVASCRIPT FOR STUDENTS        JAVASCRIPT FOR STUDENTS         JAVASCRIPT FOR STUDENTS    JAVASCRIPT FOR STUDENTS
  
  
  Template.students.nextStudent = function() {
    return (Number(Session.get('studentCursor')) + 10) + " - " + (Number(Session.get('studentCursor')) + 20);
  }
  
  Template.students.prevStudent = function() {
    if (Number(Session.get('studentCursor')) < 10) {
      return '';
    }
    return (Number(Session.get('studentCursor')) - 10) + " - " + (Number(Session.get('studentCursor')));
  }
  
  Template.students.events({
    'click .addStudent':function(evt, tmpl){
      Session.set('editing_student', false);
      mySetText('sprompt', "Adding Student");
    },
    'click .previous ':function(evt, tmpl){
      if (Number(Session.get('studentCursor')) > 9) {
        Session.set('studentCursor', Number(Session.get('studentCursor')) -10);
      }
    },
    'click .next ':function(evt, tmpl){
        Session.set('studentCursor', Number(Session.get('studentCursor')) +10);
    }
  })
  
  Template.studentRow.events({
    'dblclick .studentRow':function(evt, tmpl){
      Session.set('editing_student', tmpl.data._id);     
      mySetText('sprompt','Editing Student');
      var student = Students.findOne({_id:tmpl.data._id});       
      
      $('.cell').val(student.cell);
      $('.name').val(student.name);
      $('.login').val(student.login);
      $('.pword').val(student.pword);
      $('.sel-timez').val(student.tzoffset)
      
      if (student.allowaudio == true) {
             document.getElementById('allowaudio').checked = 1;
      } else {
             document.getElementById('allowaudio').checked = 0;
      }
      myClearAlert();

    }
  })
  
  Template.students.editing_student = function() {
    return Session.get('editing_student');
  }
  
  Template.students.studentList = function() {
     return Students.find({});
  }
  
  
  Template.students.events({
    'click .save':function(evt, tmpl) {
      var cell = tmpl.find('.cell').value;
      var name = tmpl.find('.name').value;
      var login = tmpl.find('.login').value;
      var pword = tmpl.find('.pword').value;  
      var tzoffset = tmpl.find('.sel-timez').value;
      var allowaudio = tmpl.find('.allowaudio').checked;
      var success = false;
      
     if (Session.get('editing_student')) {
        success = updateStudent(cell, name, login, pword, tzoffset, allowaudio)
        if (success == false) {
          return;
        }
        myAlert("Student Updated");
        mySetText('sprompt', 'Add Student');
        clearForm();
      } else {
        success = addStudent(cell, name, login, pword, tzoffset, allowaudio);
        if (success == false) {
          return;
        myAlert("Student Added");
        clearForm();
        mySetText('sprompt', "Add Student");
        }
      }
      Session.set('editing_student', false);
      Session.set('showStudentDialog', false);
    },
    'click .cancel':function(evt, tmpl) {
      Session.set('editing_student', false);
      mySetText('sprompt', "Add Student");
      clearForm();
      myClearAlert();
    },
    'click .remove':function(evt, tmpl) {
      removeStudent();
      Session.set('editing_student', false);
      mySetText('sprompt', "Add Student");      
      clearForm();
    },
    'click .close':function(evt, tmpl) {
      mySetText('sprompt', "Add Student");
    },
    'click .addStudent':function(evt, tmpl){
  
      mySetText('sprompt', "Adding Student");
      myClearAlert();
    }
  })

  Template.students.showStudentDialog = function(){
    return Session.get('showStudentDialog');
  }
  
  var addStudent = function(cell, name, login, pword, tzoffset, allowaudio) { 
    if (cell.length == 0) {
      myRedAlert("Cell number is required");
      return false;
    }
    
    if (phoneNumberCheck(cell) == false) {
      myRedAlert("Cell number invalid")
      return false;
    }
    
    Students.insert({cell:cell, name:name, login:login, pword:pword, tzoffset:tzoffset, allowaudio:allowaudio});
    
    myAlert("Student Inserted");
      
  }
  
  var updateStudent = function(cell, name, login, pword, tzoffset, allowaudio) {
    
    if (cell.length == 0) {
      myRedAlert("Cell number is required");
      return false;
    }
    
    if (phoneNumberCheck(cell) == false) {
      myRedAlert("Cell number invalid");
      return false;
    }    
    
    Students.update(Session.get('editing_student'), {$set: {cell:cell, name:name, login:login, pword:pword, tzoffset:tzoffset, allowaudio:allowaudio}}); 
    return true;
  }
  var clearForm = function() {
    document.getElementById('cell').value = "";
    document.getElementById('name').value = "";
    document.getElementById('login').value = "";
    document.getElementById('pword').value = "";
    document.getElementById('tzoffset').value = "";
    document.getElementById('allowaudio').checked = true;
    
    return;
  }
  
  var removeStudent = function() {
    Students.remove({_id:Session.get('editing_student')});
    myAlert("Student Removed");
  }
  
  var phoneNumberCheck = function(inputtxt) {
      var phoneno = /^\(?([0-9]{3})\)?[-]?([0-9]{3})[-]?([0-9]{4})$/;
      if (inputtxt.match(phoneno))  {  
          return true;  
        } else {  
          return false;  
        }  
  }

// MISC JAVASCRIPT USED BY EVERYTHING   MISC JAVASCRIPT USED BY EVERYTHING   MISC JAVASCRIPT USED BY EVERYTHING
// MISC JAVASCRIPT USED BY EVERYTHING   MISC JAVASCRIPT USED BY EVERYTHING   MISC JAVASCRIPT USED BY EVERYTHING
// MISC JAVASCRIPT USED BY EVERYTHING   MISC JAVASCRIPT USED BY EVERYTHING   MISC JAVASCRIPT USED BY EVERYTHING
// MISC JAVASCRIPT USED BY EVERYTHING   MISC JAVASCRIPT USED BY EVERYTHING   MISC JAVASCRIPT USED BY EVERYTHING
// MISC JAVASCRIPT USED BY EVERYTHING   MISC JAVASCRIPT USED BY EVERYTHING   MISC JAVASCRIPT USED BY EVERYTHING
  
  var myConsoleLog = function(message){
    console.log(message);
  }
  
  var myAlert = function(message) {
    document.getElementById('status').innerHTML = message;
    document.getElementById('status').style.backgroundColor = '#76EE00';
    setTimeout(myClearAlert, 3000);
  }
  
  var myRedAlert = function(message) {
    document.getElementById('status').innerHTML = message;
    document.getElementById('status').style.backgroundColor = '#FF5050';
  }
  
  var myClearAlert = function(){
    document.getElementById('status').innerHTML = "&nbsp";
    document.getElementById('status').style.backgroundColor = '#FFFFFF';
  }
  
  var myClearText = function(thisID) {
   document.getElementById(thisID).value = "";
  }
  
  var mySetText = function(thisID, thisText){
    if (thisID == "wprompt") {
        document.getElementById(thisID).innerHTML = thisText;  
    } else if (thisID == "sprompt") {
        document.getElementById(thisID).innerHTML = thisText;
    } else if (thisID == "cprompt") {
        document.getElementById(thisID).innerHTML = thisText;
    } else {
      document.getElementById(thisID).value = thisText;        
    }
      
  }
  
  var myGetText = function(thisID){
    return document.getElementById(thisID).value;
  }
  
  var myClearButton = function(thisID) {
    document.getElementById(thisID).checked = false;
  }
  
  var mySetButton = function(thisID, value) {
    document.getElementById(thisID).checked = value;
  }
  
  var myGetButton = function(thisID){
    return document.getElementById(thisID).checked;
  }
  
  var isDate = function isDate(txtDate)
  {
    var currVal = txtDate;
    if(currVal == '')
      return false;
    
    //Declare Regex  
    var rxDatePattern = /^(\d{1,2})(\/|-)(\d{1,2})(\/|-)(\d{4})$/; 
    var dtArray = currVal.match(rxDatePattern); // is format OK?
  
    if (dtArray == null)
       return false;
   
    //Checks for mm/dd/yyyy format.
    dtMonth = dtArray[1];
    dtDay= dtArray[3];
    dtYear = dtArray[5];
  
    if (dtMonth < 1 || dtMonth > 12)
        return false;
    else if (dtDay < 1 || dtDay> 31)
        return false;
    else if ((dtMonth==4 || dtMonth==6 || dtMonth==9 || dtMonth==11) && dtDay ==31)
        return false;
    else if (dtMonth == 2)
    {
       var isleap = (dtYear % 4 == 0 && (dtYear % 100 != 0 || dtYear % 400 == 0));
       if (dtDay> 29 || (dtDay ==29 && !isleap))
            return false;
    }
    return true;
}

  
  //JAVASCRIPT FOR WORD GROUPS         JAVASCRIPT FOR WORD GROUPS         JAVASCRIPT FOR WORD GROUPS
  //JAVASCRIPT FOR WORD GROUPS         JAVASCRIPT FOR WORD GROUPS         JAVASCRIPT FOR WORD GROUPS  
  //JAVASCRIPT FOR WORD GROUPS         JAVASCRIPT FOR WORD GROUPS         JAVASCRIPT FOR WORD GROUPS
  //JAVASCRIPT FOR WORD GROUPS         JAVASCRIPT FOR WORD GROUPS         JAVASCRIPT FOR WORD GROUPS
  //JAVASCRIPT FOR WORD GROUPS         JAVASCRIPT FOR WORD GROUPS         JAVASCRIPT FOR WORD GROUPS  
  //JAVASCRIPT FOR WORD GROUPS         JAVASCRIPT FOR WORD GROUPS         JAVASCRIPT FOR WORD GROUPS
  
  //
  // Highlight one row at a time    NOT WORKING YET
    var setHighLight = function(thisID){
      if (thisID == "") {
        return;
      }
      var p1 = "";
      p1 = document.getElementById('highlight').innerHTML;
      if (p1 == "") {
        
      } else {
        document.getElementById(p1).style.backgroundColor = '#FFFFFF'; 
      }
  
      document.getElementById(thisID).style.backgroundColor ='#FF7F00';
      document.getElementById('highlight').innerHTML  = thisID;
      
      return;
    }

// Determine next sequence number for new wordgroup
//
    var getNextSeqNum = function() {
      
      var lastNum = 10000;
      var nextNum = "10001";     
      var wlist = Words.find({}, {sort:{'seqnum' :1}});
      
      wlist.forEach(function(wgroup) {
        lastNum = wgroup.seqnum;
      });
      

      nextNum  = Number(lastNum) + 1;
      nextNum = $.trim(nextNum);

      return nextNum; 
    }
    
// Move WordGroup Up or Down One row
// direction is  "UP"   or "DOWN" 
//
    var moveRow = function(currentSeq, direction){
        
      var d = 1;
      if (direction =="DOWN") {
        d = -1;
      }
      
      var wlist = Words.find({}, {sort:{'seqnum' :d}});
      
      // Need to find sequence number of record before and after this one
      var previousSeq = "";
      var previousId = "";
      var currentId = "";
      var found = false;
      
      var i = 0;
      wlist.forEach(function(wgroup) { 
        
        if (found == false) {
          if (currentSeq == wgroup.seqnum) {
            found = true;
            currentId = wgroup._id;
          }
          if (found == false) {
          previousSeq = wgroup.seqnum;
          previousId = wgroup._id;
          }
        }   
      });
          
      if (previousId == "") {    // No where to move to
        return false;
      }
      
      var retVal = Words.update(previousId, {$set:{seqnum:currentSeq}});

      retVal = Words.update(currentId, {$set:{seqnum:previousSeq}});
      
      Session.set('editing_word', currentId);
      
      displayWordGroupFromDB(currentId);
      
      setHighLight(currentId);
    
                                     
      return true;
    }
 
 
 // Add New Word Group to Database
 //
    var addWord = function(seqnum, word, active, points, instruction, flashtime, use1, use2, use3,
                          question, ans1, active1, ans2, active2, ans3, active3, ans4, active4,
                          ans5, active5, remedifcorrect, remedifwrong, enableaudio, url, campaign) {         
    if (word.length == 0) {
      myRedAlert("Word is required");
      return false;
    }
    
    Words.insert({seqnum:seqnum, word:word, active:active, points:points, instruction:instruction,
                          flashtime:flashtime, use1:use1, use2:use2, use3:use3,
                          question:question, ans1:ans1, active1:active1, ans2:ans2,
                          active2:active2, ans3:ans3, active3:active3, ans4:ans4, active4:active4,
                          ans5:ans5, active5:active5, remedifcorrect:remedifcorrect,
                          remedifwrong:remedifwrong, enableaudio:enableaudio, url:url, campaign:campaign});
    
    myAlert("Word Group Inserted");
    return true;
      
  }
  
 var clearWordForm = function() {
      myClearText('wseqnum');
      myClearText('word');
      myClearButton('wactive');
      myClearText('wpoints');
      myClearText('winstruction');
      myClearText('wflashtime');
      myClearText('wuse1');
      myClearText('wuse2');
      myClearText('wuse3');
      myClearText('wquestion');
      myClearText('wans1');
      myClearButton('wactive1');
      myClearText('wans2');
      myClearButton('wactive2');
      
      myClearText('wans3');
      myClearButton('wactive3');
      
      myClearText('wans4');
      myClearButton('wactive4');
      
      myClearText('wans5');
      myClearButton('wactive5');
      
      myClearText('wremedifcorrect');
      myClearText('wremedifwrong');
      
      myClearButton('wenableaudio');
      myClearText('wurl');
      myClearText('wcampaign');
    return;
  
  }
  
  
  var updateWord = function(seqnum, word, active, points, instruction, flashtime, use1, use2, use3,
                          question, ans1, active1, ans2, active2, ans3, active3, ans4, active4,
                          ans5, active5, remedifcorrect, remedifwrong, enableaudio, url, campaign) { 
    
     if (word.length == 0) {
      myRedAlert("Word is required");
      return false;
    }
    
    Words.update(Session.get('editing_word'), {$set: {seqnum:seqnum, word:word, active:active, points:points, instruction:instruction,
                          flashtime:flashtime, use1:use1, use2:use2, use3:use3,
                          question:question, ans1:ans1, active1:active1, ans2:ans2,
                          active2:active2, ans3:ans3, active3:active3, ans4:ans4, active4:active4,
                          ans5:ans5, active5:active5, remedifcorrect:remedifcorrect,
                          remedifwrong:remedifwrong, enableaudio:enableaudio, url:url, campaign:campaign}});
    
    return true;
  }
  
    
  var removeWord = function() {
    Words.remove({_id:Session.get('editing_word')});
    myAlert("Word Group Removed");
    document.getElementById('highlight').innerHTML  = "";
  }
  
  //  Read WordGroup from database and fill display
  var displayWordGroupFromDB = function(id){
       
      var word = Words.findOne({_id:id});
      
      mySetText('wseqnum',word.seqnum);
      mySetText('word', word.word);
      mySetButton('wactive', word.active);
      mySetText('wpoints', word.points);
      mySetText('winstruction', word.instruction);
      mySetText('wflashtime', word.flashtime);
      mySetText('wuse1', word.use1);
      mySetText('wuse2', word.use2);
      mySetText('wuse3', word.use3);
      mySetText('wquestion', word.question);
      
      mySetText('wans1', word.ans1);
      mySetButton('wactive1', word.active1);
       
      mySetText('wans2', word.ans2);
      mySetButton('wactive2', word.active2);
      
      mySetText('wans3', word.ans3);
      mySetButton('wactive3', word.active3);
      
      mySetText('wans4', word.ans4);
      mySetButton('wactive4', word.active4);      
      
      mySetText('wans5', word.ans5);
      mySetButton('wactive5', word.active5);  
                  
      mySetText('wremedifcorrect',word.remedifcorrect);
      mySetText('wremedifwrong', word.remedifwrong);
      
      mySetButton('wenableaudio', word.enableaudio);
      mySetText('wurl', word.url);
      mySetText('wcampaign', word.campaign);
    
    
  }
  
 
  
  Template.wordgroups.editing_word = function() {
    return Session.get('editing_word');
  }
  
  Template.wordgroups.wordList = function() {
    
   return Words.find({}, {sort:{'seqnum' :1}});
  
  }
  
  
  Template.wordgroups.campaignList = function() {
    return Campaigns.find({}, {sort:{'campaign' :1}});
  }
    
    
  Template.wordRow.events({
    'dblclick .wordRow':function(evt, tmpl){
      
      setHighLight(tmpl.data._id);

      Session.set('editing_word', tmpl.data._id);
      mySetText('wprompt', "Editing Word Group");
      
      displayWordGroupFromDB(tmpl.data._id);
         
    },
    'click .remove':function(evt, tmpl) {
      removeWord();
      Session.set('editing_word', false);
      mySetText('wprompt', 'Add Word Group');
      clearForm();
    },
    'click .enablewordshort':function(evt, tmpl) {
      var buttonID = "B" + tmpl.data._id;
      var buttonValue = myGetButton(buttonID);
      var retVal = Words.update(tmpl.data._id, {$set:{active:buttonValue}});
    }
  
    
  })

    Template.wordgroups.events({
    'click .addWord':function(evt, tmpl){
      Session.set('editing_word', false);
      clearWordForm();
      mySetText('wprompt', "Adding Word Group");
    }, 
    'click .save':function(evt, tmpl) {
      var word = myGetText('word');
      word = word.trim();
      var seqnum = myGetText('wseqnum').trim();
      var active = myGetButton('wactive');
      var points = myGetText('wpoints');
      var instruction = myGetText('winstruction');
      var flashtime = myGetText('wflashtime');
      var use1 = myGetText('wuse1');
      var use2 = myGetText('wuse2');
      var use3 = myGetText('wuse3');
      var question = myGetText('wquestion');
  
      var ans1 = myGetText('wans1');
      var active1 = myGetButton('wactive1');
      
      var ans2 = myGetText('wans2');
      var active2 = myGetButton('wactive2');      
      
      var ans3 = myGetText('wans3');
      var active3 = myGetButton('wactive3');
       
      var ans4 = myGetText('wans4');
      var active4 = myGetButton('wactive4');     
       
      var ans5 = myGetText('wans5');
      var active5 = myGetButton('wactive5');
   
      var remedifcorrect = myGetText('wremedifcorrect');
      var remedifwrong = myGetText('wremedifwrong');
      
      var enableaudio = myGetButton('wenableaudio');
      var url = myGetButton('wurl');
      
      var campaign = myGetText('wcampaign');
               
     if (Session.get('editing_word')) {

        success = updateWord(seqnum, word, active, points, instruction, flashtime, use1, use2, use3,
                          question, ans1, active1, ans2, active2, ans3, active3, ans4, active4,
                          ans5, active5, remedifcorrect, remedifwrong, enableaudio, url, campaign);
        if (success == false) {
          return;
        }
        myAlert("Word Updated");
        clearWordForm();
        mySetText('wprompt', "Add Word Group");
        
      } else {
        var res = Words.findOne({word:word});
        
        if (res) {
          if (res.word == word) {
            myRedAlert("Words cannot be duplicated");
            return;
          }         
        }
        
        seqnum = getNextSeqNum();
        success = addWord(seqnum, word, active, points, instruction, flashtime, use1, use2, use3,
                          question, ans1, active1, ans2, active2, ans3, active3, ans4, active4,
                          ans5, active5, remedifcorrect, remedifwrong, enableaudio, url, campaign);
        if (success == false) {
          return;
        myAlert("Word Added");
        clearWordForm();
        mySetText('wprompt', 'Add Word Group');
        
        }
      }
      Session.set('editing_word', false);
    },
    'click .clear':function(evt, tmpl) {
      clearWordForm();first

      
    },
    'click .cancel':function(evt, tmpl) {
      Session.set('editing_word', false);
      mySetText('wprompt', "Add Word Group");  
      clearWordForm();
      myClearAlert();
    },
    'click .remove':function(evt, tmpl) {
      removeWord();
      Session.set('editing_word', false);
      mySetText('wprompt', "Add Word Group");       
      clearWordForm();
    },
    'click .close':function(evt, tmpl) {
    },
    'click .moveup':function(evt, tmpl) {
      var r = myGetText('wseqnum');
      var retVal = moveRow(r, "UP");
      
      if (retVal == true) {
        myAlert("Word Group Moved Up");
      } else {
        myRedAlert("Word Group Not Moved!");
      }
    },
    'click .movedown':function(evt, tmpl) {
      var r = myGetText('wseqnum');
      var retVal = moveRow(r, "DOWN");
      if (retVal == true) {
        myAlert("Word Group Moved Down")
      } else {
        myRedAlert("Word Group Not Moved!")
      }
    },
    'click .addStudent':function(evt, tmpl){
      alert('.addstudent');
      myClearAlert();
    },
    'click .addcampaign':function(evt, tmpl){
      myConsoleLog("addcampaignbutton");
      var campi = document.getElementById("campaignsBot").selectedIndex;
      var campval = document.getElementById("campaignsBot").options[campi].value;
      campAddTo(campval);
      campRender();
    } ,
     'click .removecampaign':function(evt, tmpl){
      myConsoleLog("removecampaignbutton");
      var campi = document.getElementById("campaignsBot").selectedIndex;
      var campval = document.getElementById("campaignsBot").options[campi].value;
      campRemove(campval);
      campRender();
    } ,   
    'click .clearcampaign':function(evt, tmpl){
      campClear();
    }       
    
  })
    //
    // Add campaign to this Word Group (checking for duplicates)
    var campAddTo = function(thisCamp) {
      
      myConsoleLog("campAddTo  thisCamp ->" + thisCamp);
      var curcamp = "";
      curcamp = myGetText('wcampaignids');
      
      if (curcamp == null)  {
        curcamp = ""
      }
      
      if (curcamp.contains(thisCamp) == true) {
        return;
      }
      
      curcamp = curcamp + thisCamp + ",";
      myConsoleLog("campAddTo.curcamp " + curcamp);
      mySetText('wcampaignids', curcamp);
      return;
    }
    
    //
    // Remove all Campaigns from this Word Group
    var campClear = function() {
      mySetText('wcampaignids', "");
      mySetText('wcampaign', "");
    }
    
    //
    // Remove this Campaign from this Word Group
    var campRemove = function(thisCamp) {
      var camp = thisCamp + ",";
      var allCamps = myGetText('wcampaignids');
      allCamps = allCamps.replace(camp, "");
      mySetText('wcampaignids', allCamps);
      myConsoleLog(camp + " was removed from " + allCamps);
    }
    
    //
    //Render all Campaign names on Screen for this Word Group
    var campRender = function() {
      var campList = myGetText('wcampaignids');
      
      myConsoleLog("Pre Render campaign ids  " + campList);
      
      if (campList == null) {
        mySetText('wcampaign', "");
        return;
      }
      
      var campListArray = campList.split(',');
      var campNameList = "";
      for (var i = 0; i < campListArray.length; i++) {
        myConsoleLog("This ID -> " + campListArray[i]);
        
        campNameList = campNameList + getCampaignName(campListArray[i]) + "\r\n";
      }
      
      mySetText('wcampaign', campNameList);
    }
    
    
    
    
     //JAVASCRIPT FOR Campaigns         JAVASCRIPT FOR Campaigns          JAVASCRIPT FOR Campaigns
     //JAVASCRIPT FOR Campaigns         JAVASCRIPT FOR Campaigns          JAVASCRIPT FOR Campaigns
     //JAVASCRIPT FOR Campaigns         JAVASCRIPT FOR Campaigns          JAVASCRIPT FOR Campaigns
     //JAVASCRIPT FOR Campaigns         JAVASCRIPT FOR Campaigns          JAVASCRIPT FOR Campaigns     
     //JAVASCRIPT FOR Campaigns         JAVASCRIPT FOR Campaigns          JAVASCRIPT FOR Campaigns 
 //
 // Get Campaign Name from DB Campaign Table
    var getCampaignName = function(campaignID){
      
      if (campaignID == null ){
        return "";
      }
      
      if (campaignID == "") {
        return "";
      }
      myConsoleLog("getCampaignName for id " + campaignID);   
      var campaign = Campaigns.findOne({_id:campaignID});
      
      myConsoleLog("getCampaignName return " + campaign.campaign);
      return campaign.campaign;
      
     
    }
    
  
   var clearCampaignForm = function() {
      myClearText('ccampaign');
      myClearText('ckeyword');
      
      myClearText('csequencetext');
      myClearText('imessage');
      myClearButton('monactive');
      myClearButton('tueactive');
      myClearButton('wedactive');
      myClearButton('thuactive');
      myClearButton('friactive');
      myClearButton('satactive');
      myClearButton('sunactive');
      myClearText('sendtime');
      myClearButton('studentactive');
      myClearText('sendcount');
      myClearText('sendaftercount');
      myClearText('xdate');
      myClearText('xdatelist');      
  
    return;
  
  }    
    
    
    
 // Add New Word Group to Database
 //
    var addCampaign = function(campaign, keyword, csequencetext, imessage, monactive, tueactive, wedactive,
                        thuactive, friactive, satactive, sunactive, sendtime, studentactive, sendcount, sendaftercount,
                        xdate, xdatelist) {      
    if (campaign.length == 0) {
      myRedAlert("Campaign is required");
      return false;
    }
    
    Campaigns.insert({campaign:campaign, keyword:keyword, 
                     csequencetext:csequencetext, imessage:imessage, monactive:monactive, tueactive:tueactive,
                     wedactive:wedactive, thuactive:thuactive, friactive:friactive, satactive:satactive,
                     sunactive:sunactive, sendtime:sendtime, studentactive:studentactive, sendcount:sendcount,
                     sendaftercount:sendaftercount, xdate:xdate, xdatelist:xdatelist                    
                     });
    
    myAlert("Campaign Inserted");
    return true;
      
  }

  
  var updateCampaign = function(campaign, keyword, csequencetext, imessage, monactive, tueactive, wedactive,
                        thuactive, friactive, satactive, sunactive, sendtime, studentactive, sendcount, sendaftercount,
                        xdate, xdatelist) { 
    
     if (campaign.length == 0) {
      myRedAlert("Campaign is required");
      return false;
    }

    Campaigns.update(Session.get('editing_campaign'), {$set: {campaign:campaign, keyword:keyword,
                     csequencetext:csequencetext, imessage:imessage, monactive:monactive, tueactive:tueactive,
                     wedactive:wedactive, thuactive:thuactive, friactive:friactive, satactive:satactive,
                     sunactive:sunactive, sendtime:sendtime, studentactive:studentactive, sendcount:sendcount,
                     sendaftercount:sendaftercount, xdate:xdate, xdatelist:xdatelist}});
    
    return true;
  }
  
    
  var removeCampaign = function() {
    Campaigns.remove({_id:Session.get('editing_campaign')});
    myAlert("Campaign Removed");
    document.getElementById('highlight').innerHTML  = "";
  }
  
  //  Read WordGroup from database and fill display
  var displayCampaignFromDB = function(id){
          
      var campaign = Campaigns.findOne({_id:id});
            
      mySetText('ccampaign',campaign.campaign);
      mySetText('ckeyword', campaign.keyword);
      mySetText('csequencetext', campaign.csequencetext);
      mySetText('imessage', campaign.imessage);
     
      mySetButton('monactive', campaign.monactive);
      mySetButton('tueactive', campaign.tueactive);
      mySetButton('wedactive',campaign.wedactive);
      mySetButton('thuactive', campaign.thuactive);
      mySetButton('friactive', campaign.friactive);
      mySetButton('satactive', campaign.satactive);
      mySetButton('sunactive', campaign.sunactive);
      mySetText('sendtime', campaign.sendtime);
      mySetButton('studentactive', campaign.studentactive);
      mySetText('sendcount', campaign.sendcount);
      mySetText('sendaftercount', campaign.sendaftercount);
      mySetText('xdate', campaign.xdate);
      mySetText('xdatelist', campaign.xdatelist);          
  }
    
  Template.campaigns.nextCampaign = function() {
    return (Number(Session.get('campaignCursor')) + 10) + " - " + (Number(Session.get('campaignCursor')) + 20);
  }
  
  Template.campaigns.prevCampaign = function() {
    if (Number(Session.get('campaignCursor')) < 10) {
      return '';
    }
    return (Number(Session.get('campaignCursor')) - 10) + " - " + (Number(Session.get('campaignCursor')));
  }
 
  
  Template.campaigns.editing_campaign = function() {
    return Session.get('editing_campaign');
  }
  
  Template.campaigns.campaignList = function() {
  //  return Campaigns.find({}, {sort:{'campaign' :1}});
      return Campaigns.find({});
  }
    
  Template.campaignRow.events({
    'dblclick .campaignRow':function(evt, tmpl){
      setHighLight(tmpl.data._id);

      Session.set('editing_campaign', tmpl.data._id);
      mySetText('cprompt', "Editing Campaign");
      
      displayCampaignFromDB(tmpl.data._id);
         
    }  
  })

    Template.campaigns.events({
    'click .addCampaign':function(evt, tmpl){
      Session.set('editing_campaign', false);
      clearCampaignForm();
      mySetText('cprompt', "Adding Campaign");
    },
    'click .previous ':function(evt, tmpl){
      if (Number(Session.get('campaignCursor')) > 9) {
        Session.set('campaignCursor', Number(Session.get('campaignCursor')) -10);
      }
    },
    'click .next ':function(evt, tmpl){
        Session.set('campaignCursor', Number(Session.get('campaignCursor')) +10);
    },    
    'click .save':function(evt, tmpl) {
      var campaign = myGetText('ccampaign');
      var keyword = myGetText('ckeyword');
      var sequencetext = myGetText('csequencetext');

      var imessage = myGetText('imessage');
      
      var monactive = myGetButton('monactive');
      var tueactive = myGetButton('tueactive');
      var wedactive = myGetButton('wedactive');
      var thuactive = myGetButton('thuactive');
      var friactive = myGetButton('friactive');
      var satactive = myGetButton('satactive');
      var sunactive = myGetButton('sunactive');
      
      var sendtime = myGetText('sendtime');
      var activestudent = myGetText('studentactive');
      var sendcount = myGetText('sendcount');
      var sendaftercount = myGetText('sendaftercount');
      var xdate = myGetText('xdate');
      var xdatelist = myGetText('xdatelist');
                            
     if (Session.get('editing_campaign')) {

        success = updateCampaign(campaign, keyword, sequencetext, imessage, monactive, tueactive, wedactive,
                  thuactive, friactive, satactive, sunactive, sendtime, activestudent, sendcount, sendaftercount,
                  xdate, xdatelist);
        
        if (success == false) {
          return;
        }
        myAlert("Campaign Updated");
        clearCampaignForm();
        mySetText('cprompt', "Add Campaign");
        
      } else {
        var res = Campaigns.findOne({campaign:campaign});
        
        if (res) {
          if (res.campaign == campaign) {
            myRedAlert("Campaigns cannot be duplicated");
            return;
          }         
        }
        
        success = addCampaign(campaign, keyword, sequencetext, imessage, monactive, tueactive, wedactive,
                  thuactive, friactive, satactive, sunactive, sendtime, activestudent, sendcount, sendaftercount,
                  xdate, xdatelist);      

        if (success == false) {
          return;
        myAlert("Campaign Added");
        clearCampaignForm();
        mySetText('cprompt', 'Add Campaign');
        
        }
      }
      Session.set('editing_campaign', false);
    },
    'click .clear':function(evt, tmpl) {
      clearCampaignForm();
    },
    'click .cancel':function(evt, tmpl) {
      Session.set('editing_campaign', false);
      mySetText('cprompt', "Add Campaign");  
      clearCampaignForm();
      myClearAlert();
    },
    'click .remove':function(evt, tmpl) {
      removeCampaign();
      Session.set('editing_campaign', false);
      mySetText('cprompt', "Add Campaign");       
      clearCampaignForm();
    },
    'click .addxdate':function(evt, tmpl) {
      var xdate = myGetText('xdate').trim();
      var xdatelist = myGetText('xdatelist');
            
      if (isDate(xdate) == false) {
        myRedAlert("Exclude Date Entered is invalid         mm/dd/yyyy");
        return;
      }     
      if (xdatelist.contains(xdate)) {
        myAlert("Date already on excluded list");
        return;
      }     
      xdatelist = xdatelist + xdate + " ";
      mySetText('xdatelist', xdatelist);
    },
    'click .removexdate':function(evt, tmpl) {
      var xdate = myGetText('xdate').trim();
      var xdatelist = myGetText('xdatelist');
            
      if (isDate(xdate) == false) {
        myRedAlert("Exclude Date Entered is invalid         mm/dd/yyyy");
        return;
      }
      if (xdatelist.contains(xdate) == false) {
        myRedAlert("Date not on excluded list");
        return;
      } 
      xdate = xdate + " ";
      xdatelist = xdatelist.replace(xdate, "");
      mySetText('xdatelist', xdatelist);
    },
   'click .clearxdates':function(evt, tmpl) {
      mySetText('xdatelist', "");
    }, 
    'click .seqmsginsert':function(evt, tmpl) {
      var msg = myGetText('imessage').trim();
      var msglist = myGetText('csequencetext')  
 
      msglist = msglist + msg + ";";
      mySetText('csequencetext', msglist);
    },
    'click .seqmsgremove':function(evt, tmpl) {
      var msg = myGetText('imessage').trim();
      var msglist = myGetText('csequencetext');           
      if (msglist.contains(msg) == false) {
        myRedAlert("Message already present");
        return;
      } 
      msg = msg + ";";
      msglist = msglist.replace(msg, "");
      mySetText('csequencetext', msglist);
    },
   'click .seqmsgclear':function(evt, tmpl) {
      mySetText('csequencetext', "");
    },
   'keydown .searchstring':function(evt, tmpl) {
      alert("Search String");
    },
    
   'click .close':function(evt, tmpl) {
    },
  })
     
     
     
     
     
};