import React, { useEffect, useState } from 'react'
import { db } from './services/Firestore'


const App = () => {
  const [users, setUsers] = useState([])
  const fetchUsers = async () => {
    const snapshot = await db.collection('users').get()
    const temp = []
    snapshot.docs.forEach((doc) => {
      temp.push(doc.data())
    })
    setUsers(temp)
  }
  useEffect(() => {
    fetchUsers()
  }, [])

  return (
    <div>
      <h1 style={{ textAlign: "center" }}>Welcome to WePump Admin Panel</h1>
      <div style={{ textAlign: "center" }}>
        {
          users && users.map((doc, idx) => {
            return (
              <div key={idx}>
                <h4>{doc.email_id}</h4>
                <p>{doc.status}</p>
              </div>
            )
          })
        }
      </div>
    </div>
  );
};

export default App