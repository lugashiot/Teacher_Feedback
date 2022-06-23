# Teacher_Feedback

This Github is used for a school project.
The Project is supposed to let students give their teachers a 100% anonymous feedback on a Website.
The Teacher should be able to look at some graphs of how his Students voted the questions and a text-style feedback.
In our recent version the teacher is able to create questions and polls, use his or default questions in his poll, give the poll a name and assign classes to the poll.
He is able to login with the school intern email-adress but with a different password. This password is changeable by the teacher himself.

The student recieves an email with a universally unique id. This uuid is linked to a poll id in the Database.
His answers are stored with the uuid, but the uuid doesn't know to which email-adress it was sent. That makes is 100% untraceable.
The only possiblity to find out who used the uuid/link is by checking into the django logs and getting the IP-Adress who made the request.


Our Application is based on the Django Python Framework.  
  
Credit: Pockstaller Lucas and Eder Tobias  
Teacher: Alexander Jäger
