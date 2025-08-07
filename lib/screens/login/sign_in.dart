import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import '../../_env/env.dart';
import '../../utils/avatar.dart';
import '../../utils/colors/colors.dart';
import '../../utils/responsive.dart';
import '../../widgets/long_button.dart';
import 'loginwithgoogle.dart';
import 'ordivider.dart';
import 'otp.dart';

class SignIn extends StatefulWidget {
  const SignIn({super.key});

  @override
  State<SignIn> createState() => _SignUpState();
}

class _SignUpState extends State<SignIn> {
  final formKey = GlobalKey<FormState>();
  final TextEditingController emailController = TextEditingController();
  final TextEditingController passwordController = TextEditingController();
  bool isLoading = false;
  String? errorMessage;

  Future<void> login() async {
    setState(() {
      isLoading = true;
      errorMessage = null;
    });
    final email = emailController.text.trim();
    final password = passwordController.text.trim();
    if (email.isEmpty || password.isEmpty) {
      setState(() {
        isLoading = false;
        errorMessage = 'Email and password are required.';
      });
      return;
    }
    try {
      final response = await http.post(
        Uri.parse(BaseUrl.login),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'email': email, 'password': password}),
      );
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final token = data['token'];
        // Store token securely (e.g., SharedPreferences or flutter_secure_storage)
        // For demo: print(token)
        // Navigate to home/dashboard
        if (!mounted) return;
        Navigator.pushReplacementNamed(context, '/home');
      } else {
        setState(() {
          errorMessage = 'Invalid credentials or server error.';
        });
      }
    } catch (e) {
      setState(() {
        errorMessage = 'Network error. Please try again.';
      });
    } finally {
      setState(() {
        isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    Measurements size = Measurements(MediaQuery.of(context).size);

    return Scaffold(
      backgroundColor: thirdColor,
      body: SafeArea(
        child: Form(
          key: formKey,
          child: SingleChildScrollView(
            child: Padding(
              padding: EdgeInsets.symmetric(horizontal: size.wp(5)),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  SizedBox(height: size.hp(2)),
                  Center(
                    child: Image.asset(
                      signup,
                      height: size.hp(35),
                      width: size.wp(75),
                      fit: BoxFit.contain,
                    ),
                  ),
                  SizedBox(height: size.hp(2)),
                  Text(
                    'Login',
                    style: TextStyle(
                      fontFamily: 'Roboto',
                      color: primaryColor,
                      fontSize: size.hp(3),
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  SizedBox(height: size.hp(1)),
                  Container(
                    height: size.hp(0.4),
                    width: size.wp(6),
                    decoration: BoxDecoration(
                      color: secondaryColor,
                      borderRadius: BorderRadius.circular(5),
                    ),
                  ),
                  SizedBox(height: size.hp(3)),
                  Column(
                    children: [
                      SizedBox(
                        width: size.wp(80),
                        child: TextFormField(
                          controller: emailController,
                          keyboardType: TextInputType.emailAddress,
                          decoration: InputDecoration(
                            icon: Icon(Icons.email_outlined,
                                color: primaryColor, size: size.hp(3)),
                            labelText: 'Email ID',
                            labelStyle: TextStyle(
                                color: grey2, fontWeight: FontWeight.w400),
                          ),
                        ),
                      ),
                      SizedBox(
                        width: size.wp(80),
                        child: TextFormField(
                          controller: passwordController,
                          obscureText: true,
                          keyboardType: TextInputType.text,
                          decoration: InputDecoration(
                            icon: Icon(Icons.lock_open,
                                color: primaryColor, size: size.hp(3)),
                            labelText: 'Password',
                            labelStyle: TextStyle(
                                color: grey2, fontWeight: FontWeight.w400),
                          ),
                        ),
                      ),
                      Row(
                        children: [
                          SizedBox(
                            width: size.wp(50),
                          ),
                          Text(
                            'Forgot Password?',
                            style: TextStyle(
                              color: primaryColor,
                              fontSize: size.hp(2),
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                  SizedBox(height: size.hp(4)),
                  if (errorMessage != null)
                    Padding(
                      padding: EdgeInsets.only(bottom: size.hp(2)),
                      child: Text(
                        errorMessage!,
                        style:
                            TextStyle(color: Colors.red, fontSize: size.hp(2)),
                      ),
                    ),
                  if (isLoading) Center(child: CircularProgressIndicator()),
                  SizedBox(height: size.hp(3)),
                  Center(
                    child: LongButton(
                      action: isLoading ? () {} : login,
                      text: 'Login',
                    ),
                  ),
                  SizedBox(height: size.hp(2)),
                  OrDivider(),
                  SizedBox(height: size.hp(2)),
                  GoogleAuthButton(),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}

void showCustomSnackbar(BuildContext context) {
  ScaffoldMessenger.of(context).showSnackBar(
    SnackBar(
      content: Row(
        children: [
          Icon(Icons.check_circle, color: Colors.white, size: 24),
          SizedBox(width: 10),
          Text(
            'OTP sent successfully!',
            style: TextStyle(color: Colors.white, fontSize: 16),
          ),
        ],
      ),
      backgroundColor: ColorConst.greenColor,
      behavior: SnackBarBehavior.floating,
      margin: EdgeInsets.all(16),
      elevation: 6,
      duration: Duration(seconds: 3),
    ),
  );
  Future.delayed(Duration(seconds: 3), () {
    Navigator.push(
      context,
      MaterialPageRoute(
          builder: (context) => Otp(mobile: "")), // Navigate to Otp screen
    );
  });
}
