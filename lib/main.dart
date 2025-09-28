import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:frontend/screens/login/sign_up.dart';
import 'package:frontend/screens/notes/notes.dart';
import 'package:frontend/screens/home_screen/homeScreen.dart';
import 'package:frontend/utils/session_manager.dart';
import 'package:frontend/screens/splash/splash_screen.dart';

void main() {
  runApp(
    ProviderScope(
      child: MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
        debugShowCheckedModeBanner: false, // removes debug banner
        title: 'Notes App',
        theme: ThemeData(primarySwatch: Colors.blue),
        home: const VideoSubjectScreen() // Your first screen
        );
  }
}

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  _SplashScreenState createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  @override
  void initState() {
    super.initState();
    _checkLoginStatus();
  }

  Future<void> _checkLoginStatus() async {
    await Future.delayed(const Duration(milliseconds: 500));

    if (!mounted) return;

    bool isLoggedIn = await SessionManager.isLoggedIn();

    if (isLoggedIn) {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (context) => const HomeScreen()),
      );
    } else {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (context) => const SignUp()),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    // Screen size
    final Size screenSize = MediaQuery.of(context).size;
    final double iconSize = screenSize.width * 0.25; // 25% of width
    final double fontSize = screenSize.width * 0.07; // 7% of width
    final double spacing = screenSize.height * 0.03; // 3% of height
    final double horizontalPadding = screenSize.width * 0.1; // 10% padding

    return Scaffold(
      backgroundColor: Colors.white,
      body: Center(
        child: Padding(
          padding: EdgeInsets.symmetric(horizontal: horizontalPadding),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(
                Icons.school,
                size: iconSize,
                color: Colors.teal,
              ),
              SizedBox(height: spacing),
              Text(
                'EdVoyage',
                style: TextStyle(
                  fontSize: fontSize,
                  fontWeight: FontWeight.bold,
                  color: Colors.teal,
                ),
                textAlign: TextAlign.center,
              ),
              SizedBox(height: spacing),
              SizedBox(
                width:
                    iconSize * 0.6, // responsive width for progress indicator
                height: iconSize * 0.06, // responsive height
                child: const CircularProgressIndicator(
                  color: Colors.teal,
                  strokeWidth: 4,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
