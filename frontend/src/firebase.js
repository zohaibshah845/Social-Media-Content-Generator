import { initializeApp } from 'firebase/app';
import { getAuth, signInWithEmailAndPassword, createUserWithEmailAndPassword } from 'firebase/auth';

const firebaseConfig = {
   apiKey: "AIzaSyDRxCAN8QGbZ9wF9gvPtrkGxiDsyUq43qg",
  authDomain: "social-content-generator-10e81.firebaseapp.com",
  projectId: "social-content-generator-10e81",
  storageBucket: "social-content-generator-10e81.firebasestorage.app",
  messagingSenderId: "12979678552",
  appId: "1:12979678552:web:6186022c26d45bd2de892d",
  measurementId: "G-F2QLS23SJ0"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);