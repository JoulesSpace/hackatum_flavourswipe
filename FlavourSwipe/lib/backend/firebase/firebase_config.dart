import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/foundation.dart';

Future initFirebase() async {
  if (kIsWeb) {
    await Firebase.initializeApp(
        options: const FirebaseOptions(
            apiKey: "AIzaSyAUh62tdQN-eQiFPId3-bkTqrqtq5TcEes",
            authDomain: "flavour-swipe-nmm2od.firebaseapp.com",
            projectId: "flavour-swipe-nmm2od",
            storageBucket: "flavour-swipe-nmm2od.appspot.com",
            messagingSenderId: "747241603580",
            appId: "1:747241603580:web:1ad3df9e4f2cb74064f279"));
  } else {
    await Firebase.initializeApp();
  }
}
