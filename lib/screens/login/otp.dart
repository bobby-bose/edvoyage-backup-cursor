import 'dart:convert';
import 'dart:async';
import 'package:flutter/material.dart';
import 'package:otp_text_field/otp_field.dart';
import 'package:otp_text_field/style.dart';
import 'package:http/http.dart' as http;
import '../../_env/env.dart';
import '../../utils/Toasty.dart';
import '../../utils/avatar.dart';
import '../../utils/colors/colors.dart';
import '../../utils/responsive.dart';
import '../../utils/session_manager.dart';
import '../../widgets/back_arrow_button.dart';
import '../../widgets/long_button.dart';
import '../home_screen/homeScreen.dart';
import 'package:shared_preferences/shared_preferences.dart';

class Otp extends StatefulWidget {
  final String mobile;
  const Otp({super.key, required this.mobile});

  @override
  State<Otp> createState() => _OtpState();
}

class _OtpState extends State<Otp> {
  OtpFieldController otpController = OtpFieldController();
  String otps = "";
  int attempts = 0;
  bool isBlocked = false;
  DateTime? blockedUntil;
  Timer? blockTimer;
  bool isLoading = false;

  @override
  void initState() {
    super.initState();
  }

  @override
  void dispose() {
    blockTimer?.cancel();
    super.dispose();
  }

  void showBlockedMessage() {
    if (blockedUntil != null) {
      Duration remaining = blockedUntil!.difference(DateTime.now());
      String message =
          'You have been blocked for 5 minutes due to multiple failed attempts.\n\nRemaining time: ${remaining.inMinutes}:${(remaining.inSeconds % 60).toString().padLeft(2, '0')}';

      showDialog(
        context: context,
        barrierDismissible: false,
        builder: (context) => AlertDialog(
          backgroundColor: Colors.red,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(15),
          ),
          title: Row(
            children: [
              Icon(Icons.block, color: Colors.white, size: 24),
              SizedBox(width: 10),
              Expanded(
                child: Text(
                  'Account Temporarily Blocked',
                  style: TextStyle(
                    color: Colors.white,
                    fontWeight: FontWeight.bold,
                    fontSize: 18,
                  ),
                ),
              ),
            ],
          ),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(
                Icons.timer,
                color: Colors.white,
                size: 48,
              ),
              SizedBox(height: 16),
              Text(
                message,
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 16,
                ),
                textAlign: TextAlign.center,
              ),
            ],
          ),
          actions: [
            Center(
              child: TextButton(
                onPressed: () => Navigator.pop(context),
                child: Text(
                  'OK',
                  style: TextStyle(
                    color: Colors.white,
                    fontWeight: FontWeight.bold,
                    fontSize: 16,
                  ),
                ),
              ),
            ),
          ],
        ),
      );
    }
  }

  Future<void> verifyOtp() async {
    if (isBlocked) {
      showBlockedMessage();
      return;
    }

    if (otps.length != 6) {
      Toasty.showtoast('Please enter 6-digit OTP');
      return;
    }

    setState(() {
      isLoading = true;
    });

    try {
      String deviceId = '1';

      // Check if it's the backup OTP code for testing
      if (otps == '000000') {
        print('🔍 DEBUG: Using backup OTP code for testing');
        print('🔍 DEBUG: Mobile number: ${widget.mobile}');

        // Check if user exists first
        await _checkAndCreateUser(widget.mobile, '000000');
        return;
      }

      final response = await http.post(
        Uri.parse('${BaseUrl.baseUrl}/users/otp/verify/'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'otp_code': otps,
          'contact': widget.mobile,
          'device_id': deviceId,
          'device_type': 'mobile',
        }),
      );

      final data = jsonDecode(response.body);
      print('🔍 DEBUG: OTP verification response: ${response.statusCode}');
      print('🔍 DEBUG: OTP verification data: $data');

      if (response.statusCode == 200 && data['success']) {
        print('✅ DEBUG: OTP verification successful');
        print('🔍 DEBUG: Checking if user exists in system...');

        // Check if user exists and create if needed
        await _checkAndCreateUser(widget.mobile, otps);
      } else {
        // Wrong OTP
        attempts++;
        if (attempts >= 3) {
          await handleMaxAttempts();
        } else {
          Toasty.showtoast(data['message'] ?? 'Invalid OTP');
        }
      }
    } catch (e) {
      print('❌ DEBUG: OTP verification error: $e');
      Toasty.showtoast('Network error. Please try again.');
    } finally {
      setState(() {
        isLoading = false;
      });
    }
  }

  /// Check if user exists and create if needed
  Future<void> _checkAndCreateUser(String mobile, String otpCode) async {
    try {
      print('🔍 DEBUG: Checking user existence for mobile: $mobile');

      final verifyOtpResponse = await http.post(
        Uri.parse('${BaseUrl.baseUrl}/users/otp/verify/'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'otp_code': otpCode,
          'contact': mobile,
          'device_id': '1',
          'device_type': 'mobile',
        }),
      );

      print(
          '🔍 DEBUG: OTP verification response status: ${verifyOtpResponse.statusCode}');
      print(
          '🔍 DEBUG: OTP verification response body: ${verifyOtpResponse.body}');

      if (verifyOtpResponse.statusCode == 200 ||
          verifyOtpResponse.statusCode == 201) {
        final verifyOtpData = jsonDecode(verifyOtpResponse.body);
        print('✅ DEBUG: OTP verification successful!');
        print('🔍 DEBUG: Verification data: $verifyOtpData');

        if (verifyOtpData['success']) {
          final userId = verifyOtpData['user_id'];
          final userData = verifyOtpData['user_data'];
          final userExists = verifyOtpData['user_exists'] ?? false;

          print('🔍 DEBUG: User ID: $userId');
          print('🔍 DEBUG: User data: $userData');
          print('🔍 DEBUG: User exists: $userExists');

          if (userExists) {
            print('✅ DEBUG: User exists as EXISTING user');
          } else {
            print('✅ DEBUG: User created as NEW user');
          }

          await SessionManager.storeEmail(mobile);
          Navigator.pushReplacement(
            context,
            MaterialPageRoute(builder: (context) => HomeScreen()),
          );
          Toasty.showtoast('OTP verified successfully!');
        } else {
          print(
              '❌ DEBUG: OTP verification failed: ${verifyOtpData['message']}');
          Toasty.showtoast(verifyOtpData['message'] ?? 'Failed to verify OTP');
        }
      } else {
        print(
            '❌ DEBUG: OTP verification failed with status: ${verifyOtpResponse.statusCode}');
        print('❌ DEBUG: Error response: ${verifyOtpResponse.body}');

        try {
          final errorData = jsonDecode(verifyOtpResponse.body);
          print('❌ DEBUG: Error data: $errorData');
          Toasty.showtoast(errorData['message'] ?? 'Failed to verify OTP');
        } catch (e) {
          print('❌ DEBUG: Error parsing error response: $e');
          Toasty.showtoast('Failed to verify OTP');
        }
      }
    } catch (e) {
      print('❌ DEBUG: Error in _checkAndCreateUser: $e');
      Toasty.showtoast('Network error. Please try again.');
    }
  }

  /// Store user session and navigate to home

  Future<void> handleMaxAttempts() async {
    DateTime blockUntil = DateTime.now().add(Duration(minutes: 5));
    Future<void> storeBlockTime(DateTime blockUntil) async {
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('blockUntil', blockUntil.toIso8601String());
    }

    Future<DateTime?> getBlockTime() async {
      final prefs = await SharedPreferences.getInstance();
      final blockUntilString = prefs.getString('blockUntil');
      if (blockUntilString != null) {
        return DateTime.parse(blockUntilString);
      }
      return null;
    }

    Future<void> clearBlockTime() async {
      final prefs = await SharedPreferences.getInstance();
      await prefs.remove('blockUntil');
    }

    storeBlockTime(blockUntil);

    setState(() {
      isBlocked = true;
      blockedUntil = blockUntil;
    });
    Future<void> startBlockTimer() async {
      DateTime? blockUntil = await getBlockTime();
      if (blockUntil != null) {
        Duration remaining = blockUntil.difference(DateTime.now());
        if (remaining.isNegative) {
          await clearBlockTime();
          setState(() {
            isBlocked = false;
            blockedUntil = null;
          });
        } else {
          Timer(remaining, () async {
            await clearBlockTime();
            setState(() {
              isBlocked = false;
              blockedUntil = null;
            });
          });
        }
      }
    }

    startBlockTimer();
    showBlockedMessage();
  }

  @override
  Widget build(BuildContext context) {
    Measurements size = Measurements(MediaQuery.of(context).size);
    return Scaffold(
      backgroundColor: thirdColor,
      body: SingleChildScrollView(
        child: Container(
          color: thirdColor,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.start,
            children: [
              SizedBox(height: size?.hp(5)),
              const Row(
                children: [
                  BackArrow(),
                ],
              ),
              SizedBox(
                height: size?.hp(30),
                width: size?.wp(60),
                child: Image.asset(
                  otp,
                  fit: BoxFit.cover,
                ),
              ),
              SizedBox(height: size?.hp(1)),
              Padding(
                padding: const EdgeInsets.only(left: 30),
                child: Stack(
                  children: [
                    Container(
                      height: size?.hp(5),
                      alignment: Alignment.centerLeft,
                      child: Text(
                        'Enter OTP',
                        textScaleFactor: 2.2,
                        style: TextStyle(
                          fontFamily: 'Roboto',
                          color: primaryColor,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                    Column(
                      children: [
                        SizedBox(height: size?.hp(4.5)),
                        Container(
                          margin: const EdgeInsets.only(left: 1.5),
                          height: size?.hp(.4),
                          width: size?.wp(9),
                          decoration: BoxDecoration(
                            color: secondaryColor,
                            borderRadius: BorderRadius.circular(5),
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
              SizedBox(height: size?.hp(3)),
              Padding(
                padding: const EdgeInsets.only(left: 30),
                child: Column(
                  children: [
                    Container(
                      alignment: Alignment.centerLeft,
                      child: Text(
                        "A 6 digit code has been sent to\n your mobile number: ${widget.mobile}",
                        textScaleFactor: 1.4,
                        style: TextStyle(
                          fontFamily: 'Roboto',
                          color: Color.fromARGB(255, 67, 56, 56),
                          fontWeight: FontWeight.w800,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
              SizedBox(height: size?.hp(3)),

              // Blocked status indicator
              if (isBlocked && blockedUntil != null) ...[
                Container(
                  margin: EdgeInsets.symmetric(horizontal: 30),
                  padding: EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: Colors.red.withOpacity(0.1),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: Colors.red.withOpacity(0.3)),
                  ),
                  child: Row(
                    children: [
                      Icon(Icons.block, color: Colors.red, size: 20),
                      SizedBox(width: 12),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              'Account Temporarily Blocked',
                              style: TextStyle(
                                color: Colors.red,
                                fontWeight: FontWeight.bold,
                                fontSize: 14,
                              ),
                            ),
                            SizedBox(height: 4),
                            Text(
                              'Remaining time: ${blockedUntil!.difference(DateTime.now()).inMinutes}:${(blockedUntil!.difference(DateTime.now()).inSeconds % 60).toString().padLeft(2, '0')}',
                              style: TextStyle(
                                color: Colors.red.shade700,
                                fontSize: 12,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
                SizedBox(height: size?.hp(2)),
              ],

              // OTP Input Field
              if (!isBlocked) ...[
                Padding(
                  padding: EdgeInsets.symmetric(horizontal: size!.wp(5)),
                  child: OTPTextField(
                    controller: otpController,
                    length: 6,
                    width: size!.wp(90),
                    textFieldAlignment: MainAxisAlignment.spaceEvenly,
                    fieldWidth: size!.wp(12),
                    fieldStyle: FieldStyle.box,
                    outlineBorderRadius: 10,
                    style: TextStyle(fontSize: size!.wp(5)),
                    onChanged: (value) {
                      otps = value;
                      print("OTP entered: $otps");
                    },
                  ),
                ),
                SizedBox(height: size?.hp(2)),

                // Backup OTP indicator for testing
                Container(
                  margin: EdgeInsets.symmetric(horizontal: 30),
                  padding: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                  decoration: BoxDecoration(
                    color: Colors.blue.withOpacity(0.1),
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(color: Colors.blue.withOpacity(0.3)),
                  ),
                  child: Row(
                    children: [
                      Icon(Icons.info_outline, color: Colors.blue, size: 16),
                      SizedBox(width: 8),
                      Expanded(
                        child: Text(
                          'For testing: Use backup code "000000"',
                          style: TextStyle(
                            color: Colors.blue.shade700,
                            fontSize: 12,
                            fontWeight: FontWeight.w500,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
                SizedBox(height: size?.hp(2)),

                // Attempts remaining indicator
                if (attempts > 0) ...[
                  Container(
                    margin: EdgeInsets.symmetric(horizontal: 30),
                    padding: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                    decoration: BoxDecoration(
                      color: Colors.orange.withOpacity(0.1),
                      borderRadius: BorderRadius.circular(8),
                      border: Border.all(color: Colors.orange.withOpacity(0.3)),
                    ),
                    child: Text(
                      '${3 - attempts} attempts remaining',
                      style: TextStyle(
                        color: Colors.orange.shade700,
                        fontSize: 12,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                  ),
                  SizedBox(height: size?.hp(2)),
                ],

                // Verify Button
                LongButton(
                  action: isLoading ? () {} : () => verifyOtp(),
                  text: isLoading ? 'Verifying...' : 'Verify',
                ),
              ],

              SizedBox(height: size?.hp(2)),
            ],
          ),
        ),
      ),
    );
  }
}
