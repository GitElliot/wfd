
  
   if (Meteor.isServer) {
    
      Students = new Meteor.Collection('students');
      Words = new Meteor.Collection('words');
      Campaigns = new Meteor.Collection('campaigns');
      
      WordLogs = new Meteor.Collection('wordlogs');
      
      
      Meteor.startup(function() {
        Meteor.methods({
//            removeAllStudents:function() {
//               Students.remove({});
//            }
        })
    
     });
      
      Meteor.publish("students", function(studentCursor){
          return Students.find({}, {sort:{'cell' :1}, limit:10, skip:studentCursor});
      })
           
      Meteor.publish("words", function(wordCursor){
//       return Words.find({}, {sort:{'seqnum' :1}, skip:wordCursor});  // Never really worked right          
         return Words.find({}, {sort:{'seqnum' :1}});      
      })
      
      Meteor.publish("campaigns", function(campaignCursor){
//        return Campaigns.find({}, {sort:{'campaign' :1},  skip:campaignCursor});   // Never really worked right        
        return Campaigns.find({}, {sort:{'campaign' :1}});
      })
      
      Meteor.publish("wordLogs", function(wordLogsCursor) {
         return WordLogs.find({}, {sort:{'seqnum' :1}});      
      })
      
      
      Accounts.validateNewUser(function(options, user) {
         throw new Meteor.Error(403, "New Users Can Not Be Added At This Time");
         return false;
      })
      
   }
   