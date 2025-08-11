import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:http/http.dart' as http;
import '../../_env/env.dart';
import '../../utils/avatar.dart';
import '../../utils/colors/colors.dart';
import '../../utils/responsive.dart';
import '../../utils/session_manager.dart';
import '../../utils/Toasty.dart';
import '../../widgets/long_button.dart';
import 'otp.dart';
import 'privacy_policy.dart';
import 'terms_n_condition.dart';
import 'package:get/get.dart';
import '../home_screen/homeScreen.dart';

class SignUp extends StatefulWidget {
  const SignUp({super.key});

  @override
  State<SignUp> createState() => _SignUpState();
}

class _SignUpState extends State<SignUp> {
  final TextEditingController _email = TextEditingController();
  final formKey = GlobalKey<FormState>();
  bool isLoading = false;
  bool rememberMe = false; // Add remember me state

  @override
  void initState() {
    super.initState();
    _loadStoredEmail();
  }

  /// Load stored email if available
  Future<void> _loadStoredEmail() async {
    String? storedEmail = await SessionManager.getStoredEmail();
    if (storedEmail != null && storedEmail.isNotEmpty) {
      setState(() {
        _email.text = storedEmail;
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
                    'Sign up',
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
                      color: Colors.teal,
                      borderRadius: BorderRadius.circular(5),
                    ),
                  ),
                  SizedBox(height: size.hp(3)),
                  TextFormField(
                    keyboardType: TextInputType.emailAddress,
                    controller: _email,
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return 'Enter Email Address';
                      }
                      // Basic email validation
                      if (!RegExp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$')
                          .hasMatch(value)) {
                        return 'Enter a valid email address';
                      }
                      return null;
                    },
                    decoration: InputDecoration(
                      icon: Icon(Icons.email,
                          color: primaryColor, size: size.hp(3)),
                      labelText: 'Email Address',
                      labelStyle:
                          TextStyle(color: grey2, fontWeight: FontWeight.w400),
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(8),
                        borderSide: BorderSide(color: primaryColor),
                      ),
                      focusedBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(8),
                        borderSide: BorderSide(color: primaryColor, width: 2),
                      ),
                    ),
                  ),
                  SizedBox(height: size.hp(1)),
                  // Remember Me checkbox
                  Row(
                    children: [
                      Checkbox(
                        value: rememberMe,
                        onChanged: (value) {
                          setState(() {
                            rememberMe = value ?? false;
                          });
                        },
                        activeColor: primaryColor,
                      ),
                      Text(
                        'Remember Me',
                        style: TextStyle(
                          color: grey2,
                          fontSize: size.hp(1.8),
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                    ],
                  ),
                  SizedBox(height: size.hp(1)),
                  // Container(
                  //   height: size.hp(2),
                  //   child: Column(
                  //     crossAxisAlignment: CrossAxisAlignment.start,
                  //     children: [
                  //       Wrap(
                  //         children: [
                  //           TextButton(
                  //             onPressed: () {},
                  //             child: Text('By signing up, you agree to our ',
                  //                 style: TextStyle(
                  //                   color: grey2,
                  //                   fontSize: size.hp(1.7),
                  //                 )),
                  //           ),
                  //           TextButton(
                  //             onPressed: () => Get.to(() => terms_condition()),
                  //             child: Text('Terms & Conditions',
                  //                 style: TextStyle(
                  //                     color: primaryColor,
                  //                     fontSize: size.hp(1.7))),
                  //           ),
                  //         ],
                  //       ),
                  //       Wrap(
                  //         children: [
                  //           TextButton(
                  //             onPressed: () {},
                  //             child: Text('and ',
                  //                 style: TextStyle(
                  //                     color: grey2, fontSize: size.hp(1.7))),
                  //           ),
                  //           TextButton(
                  //             onPressed: () => Get.to(() => privacy()),
                  //             child: Text('Privacy Policy',
                  //                 style: TextStyle(
                  //                     color: primaryColor,
                  //                     fontSize: size.hp(1.7))),
                  //           ),
                  //         ],
                  //       ),
                  //     ],
                  //   ),
                  // ),
                  Text(
                    "By Signing Up you agree to our terms and Conditions and Privacy Policy",
                    style: TextStyle(fontSize: size.hp(2.2)),
                  ),
                  SizedBox(height: size.hp(6)),
                  Center(
                    child: LongButton(
                      action: isLoading
                          ? () {}
                          : () =>
                              sendOtp(context, _email.text.trim(), rememberMe),
                      text: isLoading ? 'Sending OTP...' : 'Send OTP to Email',
                    ),
                  ),
                  SizedBox(height: size.hp(2)),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}

Future<void> sendOtp(
    BuildContext context, String email, bool rememberMe) async {
  if (email.isEmpty) {
    Toasty.showtoast('Please enter your email address');
    return;
  }

  // Validate email format
  if (!RegExp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$').hasMatch(email)) {
    Toasty.showtoast('Please enter a valid email address');
    return;
  }

  // Show loading state
  if (context.mounted) {
    final state = context.findAncestorStateOfType<_SignUpState>();
    if (state != null) {
      state.setState(() {
        state.isLoading = true;
      });
    }
  }

  try {
    final response = await http.post(
      Uri.parse('${BaseUrl.baseUrl}/users/otp/create/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'otp_type': 'register',
        'contact': email,
        'device_id': '1',
        'device_type': 'mobile',
      }),
    );

    if (context.mounted) {
      final state = context.findAncestorStateOfType<_SignUpState>();
      if (state != null) {
        state.setState(() {
          state.isLoading = false;
        });
      }
    }

    if (response.statusCode == 200 || response.statusCode == 201) {
      final data = jsonDecode(response.body);

      if (data['success']) {
        // Check if user already exists
        bool userExists = data['user_exists'] == true;

        if (userExists) {
          // User already exists - log them in directly
          Toasty.showtoast('Welcome back! Logging you in...');

          // Store user session data
          await SessionManager.storeEmail(email);

          // Navigate to home screen
          if (context.mounted) {
            Navigator.pushAndRemoveUntil(
                context,
                MaterialPageRoute(builder: (context) => HomeScreen()),
                (route) => false);
          }
        } else {
          // New user - send OTP
          Toasty.showtoast('OTP sent successfully to your email');

          // Store remember me preference for OTP verification
          if (rememberMe) {
            await SessionManager.storeEmail(email);
          }

          // Navigate to OTP screen
          if (context.mounted) {
            Navigator.push(
              context,
              MaterialPageRoute(builder: (context) => Otp(mobile: email)),
            );
          }
        }
      } else {
        Toasty.showtoast(data['message'] ?? 'Failed to send OTP');
      }
    } else if (response.statusCode == 429) {
      // Device blocked
      final data = jsonDecode(response.body);
      Toasty.showtoast(data['message'] ?? 'Device blocked for 5 minutes');
    } else {
      Toasty.showtoast('Failed to send OTP');
    }
  } catch (e) {
    if (context.mounted) {
      final state = context.findAncestorStateOfType<_SignUpState>();
      if (state != null) {
        state.setState(() {
          state.isLoading = false;
        });
      }
    }
    Toasty.showtoast('Network error. Please try again.');
  }
}
