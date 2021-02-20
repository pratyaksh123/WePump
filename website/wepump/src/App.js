import { FirestoreProvider, FirestoreCollection } from "@react-firebase/firestore";
import { firebaseConfig } from "./firebaseConfig"
import firebase from "firebase/app";
import 'firebase/firestore';
import { useState } from "react";

const App = () => {
  const [users, setUsers] = useState([])
  return (
    <FirestoreProvider {...firebaseConfig} firebase={firebase}>
      <div>This is my app</div>
      <FirestoreCollection path="/users/">
        {d => {
          setUsers([...users, d.value])
        }}
      </FirestoreCollection>
      {users.map((t) => {
        return <p>{t}</p>
      })}
    </FirestoreProvider>
  );
};

export default App