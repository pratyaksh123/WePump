const functions = require("firebase-functions");
const admin = require("firebase-admin");
const express = require("express");
const cors = require("cors");
const app = express();
app.use(cors({origin: true}));

const serviceAccount = require("./permissions.json");
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: "https://fir-api-9a206..firebaseio.com",
});
const db = admin.firestore();

// create
app.post("/api/register-trial", (req, res) => {
  (async () => {
    try {
      await db
          .collection("users")
          .doc("/" + req.body.mac_id + "/")
          .create({
            mac_id: req.body.mac_id,
            email_id: req.body.email_id,
            status: "Trial",
          });
      return res.status(200).send("Success");
    } catch (error) {
      console.log(error);
      return res.status(500).send(error);
    }
  })();
});
// get
app.get("/api/read/:mac_id", (req, res) => {
  (async () => {
    try {
      const document = db.collection("users").doc(req.params.mac_id);
      const item = await document.get();
      const response = item.data();
      if (response) {
        return res.status(200).send(response);
      } else {
        return res.status(200).send("Not Found");
      }
    } catch (error) {
      console.log(error);
      return res.status(500).send(error);
    }
  })();
});

// update
app.put("/api/update/:mac_id", (req, res) => {
  (async () => {
    try {
      const document = db.collection("users").doc(req.params.mac_id);
      await document.update({
        status: req.body.status,
      });
      return res.status(200).send("Success");
    } catch (error) {
      console.log(error);
      return res.status(500).send(error);
    }
  })();
});

exports.app = functions.https.onRequest(app);
