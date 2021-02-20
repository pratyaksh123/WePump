import { FirestoreProvider, FirestoreCollection } from "@react-firebase/firestore";
import { firebaseConfig } from "./firebaseConfig"
import firebase from "firebase/app";
import 'firebase/firestore';


const App = () => {
  return (
    <FirestoreProvider {...firebaseConfig} firebase={firebase}>
      <div>This is my app</div>
      <div>
        <FirestoreCollection path="/users/">

          {d => <p>{JSON.stringify(d.value)}</p>}

        </FirestoreCollection>
      </div>
    </FirestoreProvider>
  );
};

export default App