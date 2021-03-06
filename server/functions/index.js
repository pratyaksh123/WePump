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
      const document = db.collection('users').doc(req.params.mac_id);
      const item = await document.get();
      const response = item.data();
      if (response) {
        return res.status(200).send(response);
      } else {
        return res.status(200).send('Not Found');
      }
    } catch (error) {
      console.log(error);
      return res.status(500).send(error);
    }
  })();
});

// update
app.put('/api/update/:mac_id', (req, res) => {
  (async () => {
    try {
      const document = db.collection('users').doc(req.params.mac_id);
      await document.update({
        status: req.body.status,
        updation_timestamp: admin.firestore.FieldValue.serverTimestamp(),
      });
      return res.status(200).send('Success');
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

exports.app = functions.https.onRequest(app);
