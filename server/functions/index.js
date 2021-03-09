/* eslint-disable max-len */
/* eslint-disable camelcase */
const functions = require('firebase-functions');
const admin = require('firebase-admin');
const express = require('express');
const cors = require('cors');
const app = express();
app.use(cors({origin: true}));

const serviceAccount = require('./permissions.json');
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: 'https://fir-api-9a206..firebaseio.com',
});
const db = admin.firestore();

// create
app.post('/api/register-trial', (req, res) => {
  (async () => {
    try {
      await db
          .collection('users')
          .doc('/' + req.body.mac_id + '/')
          .create({
            mac_id: req.body.mac_id,
            email_id: req.body.email_id,
            password: req.body.password,
            status: 'Trial',
            creation_timestamp: admin.firestore.FieldValue.serverTimestamp(),
            expiration_timestamp: admin.firestore.Timestamp.fromDate(
                new Date(new Date().getTime() + 3 * 24 * 60 * 60 * 1000)
            ).toDate(),
          });
      return res.status(200).send('Success');
    } catch (error) {
      console.log(error);
      return res.status(500).send(error);
    }
  })();
});

// get
app.get('/api/read/:mac_id', (req, res) => {
  (async () => {
    try {
      const document_ref = db.collection('users');
      document_ref
          .where('mac_id', '==', req.params.mac_id)
          .get()
          .then((querySnapshot) => {
            if (querySnapshot.size==1) {
              querySnapshot.forEach((doc)=>{
                return res.status(200).send(doc.data());
              });
            } else {
              return res.status(200).send(false);
            }
          });
    } catch (error) {
      console.log(error);
      return res.status(500).send(error);
    }
  })();
});

app.get('/api/check_email/:email_id', (req, res) => {
  (async () => {
    try {
      const document_ref = db.collection('users');
      document_ref
          .where('email_id', '==', req.params.email_id)
          .get()
          .then((querySnapshot) => {
            if (querySnapshot.size==1) {
              return res.status(200).send(true);
            } else {
              return res.status(200).send(false);
            }
          });
    } catch (error) {
      console.log(error);
      return res.status(500).send(error);
    }
  })();
});


app.get('/api/get_password/:password', (req, res) => {
  (async () => {
    try {
      const document_ref = db.collection('users');
      document_ref
          .where('password', '==', req.params.password)
          .get()
          .then((querySnapshot) => {
            if (querySnapshot.size==1) {
              return res.status(200).send(true);
            } else {
              return res.status(200).send(false);
            }
          });
    } catch (error) {
      console.log(error);
      return res.status(500).send(error);
    }
  })();
});

// Fetch password by mac id


app.put('/api/update_mac_id/:email_id', (req, res) => {
  (async () => {
    try {
      const document_ref = db.collection('users');
      document_ref
          .where('email_id', '==', req.params.email_id)
          .get()
          .then((querySnapshot) => {
            if (querySnapshot.size==1) {
              querySnapshot.forEach((doc)=>{
                doc.ref.update({
                  mac_id: req.body.mac_id,
                });
              });
              return res.status(200).send(true);
            } else {
              return res.status(200).send(false);
            }
          });
    } catch (error) {
      console.log(error);
      return res.status(500).send(error);
    }
  })();
});

// get passowrd by mac id
app.get('/api/get_password_mac_id/:mac_id', (req, res) => {
  (async () => {
    try {
      const document_ref = db.collection('users');
      document_ref
          .where('mac_id', '==', req.params.mac_id)
          .get()
          .then((querySnapshot) => {
            if (querySnapshot.size==1) {
              querySnapshot.forEach((doc)=>{
                return res.status(200).send(doc.data().password);
              });
            } else {
              return res.status(200).send(false);
            }
          });
    } catch (error) {
      console.log(error);
      return res.status(500).send(error);
    }
  })();
});


// update password
app.put('/api/update_password/:mac_id', (req, res) => {
  (async () => {
    try {
      const document_ref = db.collection('users');
      document_ref
          .where('mac_id', '==', req.params.mac_id)
          .get()
          .then((querySnapshot) => {
            if (querySnapshot.size==1) {
              querySnapshot.forEach((doc)=>{
                doc.ref.update({
                  password: req.body.password,
                });
                return res.status(200).send('Success');
              });
            } else {
              return res.status(200).send(false);
            }
          });
    } catch (error) {
      console.log(error);
      return res.status(500).send(error);
    }
  })();
});

// clean-up DB for expired users
app.get('/api/cleanup-expired', (req, res) => {
  (async () => {
    try {
      const document_ref = db.collection('users');
      document_ref
          .where('expiration_timestamp', '<', admin.firestore.Timestamp.now())
          .get()
          .then((querySnapshot) => {
            querySnapshot.forEach((doc) => {
              if (doc.data().status=='Trial') {
                doc.ref.update({
                  status: 'Expired',
                });
              }
            });
          });
      return res.status(200).send('Updated');
    } catch (error) {
      console.log(error);
      return res.status(500).send(error);
    }
  })();
});

// Add password as 'change-me' for all docs
app.put('/api/update_password_all/', (req, res) => {
  (async () => {
    try {
      db.collection('users').get().then(function(querySnapshot) {
        querySnapshot.forEach(function(doc) {
          doc.ref.update({
            password: 'change-me',
          });
        });
      });
      return res.status(200).send('Updated');
    } catch (error) {
      console.log(error);
      return res.status(500).send(error);
    }
  })();
});


exports.app = functions.https.onRequest(app);
