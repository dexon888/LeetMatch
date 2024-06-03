// src/firebase.js
import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyBT85hVR-PcE2etW_ZjAdohLE7d387oe1I",
  authDomain: "leetmatch-8d7ee.firebaseapp.com",
  projectId: "leetmatch-8d7ee",
  storageBucket: "leetmatch-8d7ee.appspot.com",
  messagingSenderId: "249344374082",
  appId: "1:249344374082:web:abad761a675024085604db",
  measurementId: "G-39R5ELLTFT"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase Authentication and get a reference to the service
const auth = getAuth(app);
export { auth };
