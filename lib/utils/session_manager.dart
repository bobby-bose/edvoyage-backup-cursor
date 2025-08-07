import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:http/http.dart' as http;
import '../_env/env.dart';

class SessionManager {
  static const String _sessionKey = 'session_key';
  static const String _userIdKey = 'user_id';
  static const String _userDataKey = 'user_data';
  static const String _deviceIdKey = 'device_id';
  static const String _isLoggedInKey = 'is_logged_in';
  static const String _phoneNumberKey = 'phone_number';
  static const String _persistentLoginKey = 'persistent_login';
  static const String _rememberMeKey = 'remember_me';
  static const String _sessionExpiryKey = 'session_expiry';
  static const String _lastActivityKey = 'last_activity';

  /// Get or generate device ID
  static Future<String> getDeviceId() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    String? deviceId = prefs.getString(_deviceIdKey);

    if (deviceId == null) {
      deviceId = DateTime.now().millisecondsSinceEpoch.toString();
      await prefs.setString(_deviceIdKey, deviceId);
    }

    return deviceId;
  }

  /// Store user session data
  static Future<void> storeUserSession(Map<String, dynamic> data) async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    await prefs.setString(_sessionKey, data['session_key']);
    await prefs.setString(_userIdKey, data['user_id'].toString());
    await prefs.setString(_userDataKey, jsonEncode(data['user_data']));
    await prefs.setBool(_isLoggedInKey, true);

    // Set session expiry (24 hours from now)
    DateTime sessionExpiry = DateTime.now().add(Duration(hours: 24));
    await prefs.setString(_sessionExpiryKey, sessionExpiry.toIso8601String());

    // Set last activity
    await prefs.setString(_lastActivityKey, DateTime.now().toIso8601String());

    // Store phone number if available
    if (data['user_data'] != null && data['user_data']['profile'] != null) {
      String? phoneNumber = data['user_data']['profile']['phone_number'];
      if (phoneNumber != null) {
        await prefs.setString(_phoneNumberKey, phoneNumber);
      }
    }

    // Store email if available
    if (data['user_data'] != null && data['user_data']['email'] != null) {
      await prefs.setString(_phoneNumberKey, data['user_data']['email']);
    }
  }

  /// Check if user is logged in
  static Future<bool> isLoggedIn() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    bool? isLoggedIn = prefs.getBool(_isLoggedInKey);

    if (isLoggedIn == true) {
      String? sessionKey = prefs.getString(_sessionKey);
      String? userId = prefs.getString(_userIdKey);
      String? sessionExpiryStr = prefs.getString(_sessionExpiryKey);

      if (sessionKey != null && userId != null && sessionExpiryStr != null) {
        // Check if session has expired locally
        DateTime sessionExpiry = DateTime.parse(sessionExpiryStr);
        if (DateTime.now().isAfter(sessionExpiry)) {
          // Session expired, clear it
          await logout();
          return false;
        }

        // Update last activity
        await prefs.setString(
            _lastActivityKey, DateTime.now().toIso8601String());

        // For development, return true immediately (like browser sessions)
        // For production, you can uncomment the backend validation
        return true;

        // Uncomment this for production backend validation:
        // return await validateSession(sessionKey, userId);
      }
    }

    return false;
  }

  /// Validate session with backend
  static Future<bool> validateSession(String sessionKey, String userId) async {
    try {
      String deviceId = await getDeviceId();

      final response = await http.post(
        Uri.parse('${BaseUrl.baseUrl}/users/sessions/validate/'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'session_key': sessionKey,
          'device_id': deviceId,
        }),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['success'] == true;
      }

      return false;
    } catch (e) {
      print('Error validating session: $e');
      return false;
    }
  }

  /// Logout user
  static Future<void> logout() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    String? sessionKey = prefs.getString(_sessionKey);
    String? deviceId = await getDeviceId();

    if (sessionKey != null) {
      try {
        await http.post(
          Uri.parse('${BaseUrl.baseUrl}/users/sessions/logout/'),
          headers: {'Content-Type': 'application/json'},
          body: jsonEncode({
            'session_key': sessionKey,
            'device_id': deviceId,
          }),
        );
      } catch (e) {
        print('Error during logout: $e');
      }
    }

    // Clear local storage
    await prefs.remove(_sessionKey);
    await prefs.remove(_userIdKey);
    await prefs.remove(_userDataKey);
    await prefs.setBool(_isLoggedInKey, false);
    await prefs.remove(_phoneNumberKey);
  }

  /// Get user ID
  static Future<String?> getUserId() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    return prefs.getString(_userIdKey);
  }

  /// Get user data
  static Future<Map<String, dynamic>?> getUserData() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    String? userDataStr = prefs.getString(_userDataKey);
    if (userDataStr != null) {
      return jsonDecode(userDataStr);
    }
    return null;
  }

  /// Get session key
  static Future<String?> getSessionKey() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    return prefs.getString(_sessionKey);
  }

  /// Get phone number
  static Future<String?> getPhoneNumber() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    return prefs.getString(_phoneNumberKey);
  }

  /// Get stored email (same as phone number key but stores email)
  static Future<String?> getStoredEmail() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    return prefs.getString(_phoneNumberKey);
  }

  /// Store phone number
  static Future<void> storePhoneNumber(String phoneNumber) async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    await prefs.setString(_phoneNumberKey, phoneNumber);
  }

  /// Check if device is blocked for OTP
  static Future<bool> isDeviceBlocked() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    String? blockedUntilStr = prefs.getString('otp_blocked_until');

    if (blockedUntilStr != null) {
      DateTime blockedTime = DateTime.parse(blockedUntilStr);
      return DateTime.now().isBefore(blockedTime);
    }

    return false;
  }

  /// Get remaining block time
  static Future<int> getRemainingBlockTime() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    String? blockedUntilStr = prefs.getString('otp_blocked_until');

    if (blockedUntilStr != null) {
      DateTime blockedTime = DateTime.parse(blockedUntilStr);
      if (DateTime.now().isBefore(blockedTime)) {
        return blockedTime.difference(DateTime.now()).inSeconds;
      }
    }

    return 0;
  }

  /// Store block time
  static Future<void> storeBlockTime(DateTime blockedUntil) async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    await prefs.setString('otp_blocked_until', blockedUntil.toIso8601String());
  }

  /// Clear block time
  static Future<void> clearBlockTime() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    await prefs.remove('otp_blocked_until');
  }

  /// Get device type
  static String getDeviceType() {
    // This would typically use platform detection
    // For now, return 'mobile' as default
    return 'mobile';
  }

  /// Create API headers with session
  static Future<Map<String, String>> getApiHeaders() async {
    String? sessionKey = await getSessionKey();
    String deviceId = await getDeviceId();

    Map<String, String> headers = {
      'Content-Type': 'application/json',
      'Device-ID': deviceId,
      'Device-Type': getDeviceType(),
    };

    if (sessionKey != null) {
      headers['Session-Key'] = sessionKey;
    }

    return headers;
  }

  /// Add user ID to API requests
  static Future<Map<String, dynamic>> addUserIdToRequest(
      Map<String, dynamic> data) async {
    String? userId = await getUserId();
    if (userId != null) {
      data['user_id'] = userId;
    }
    return data;
  }

  /// Store persistent login data
  static Future<void> storePersistentLogin(Map<String, dynamic> data) async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    await prefs.setString(_persistentLoginKey, jsonEncode(data));
    await prefs.setBool(_rememberMeKey, true);
  }

  /// Store remember me preference
  static Future<void> storeRememberMePreference(bool rememberMe) async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    await prefs.setBool(_rememberMeKey, rememberMe);
  }

  /// Get persistent login data
  static Future<Map<String, dynamic>?> getPersistentLogin() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    String? persistentData = prefs.getString(_persistentLoginKey);
    if (persistentData != null) {
      return jsonDecode(persistentData);
    }
    return null;
  }

  /// Check if remember me is enabled
  static Future<bool> isRememberMeEnabled() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    return prefs.getBool(_rememberMeKey) ?? false;
  }

  /// Auto-login if persistent data exists
  static Future<bool> autoLogin() async {
    if (await isRememberMeEnabled()) {
      Map<String, dynamic>? persistentData = await getPersistentLogin();
      if (persistentData != null) {
        // Validate the persistent session
        String? sessionKey = persistentData['session_key'];
        String? userId = persistentData['user_id'].toString();

        if (sessionKey != null && userId != null) {
          bool isValid = await validateSession(sessionKey, userId);
          if (isValid) {
            // Restore the session
            await storeUserSession(persistentData);
            return true;
          } else {
            // Session is invalid, clear persistent data
            await clearPersistentLogin();
          }
        }
      }
    }
    return false;
  }

  /// Check if persistent login session is still valid
  static Future<bool> isPersistentSessionValid() async {
    Map<String, dynamic>? persistentData = await getPersistentLogin();
    if (persistentData != null) {
      String? sessionKey = persistentData['session_key'];
      String? userId = persistentData['user_id'].toString();

      if (sessionKey != null && userId != null) {
        return await validateSession(sessionKey, userId);
      }
    }
    return false;
  }

  /// Clear persistent login data
  static Future<void> clearPersistentLogin() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    await prefs.remove(_persistentLoginKey);
    await prefs.remove(_rememberMeKey);
  }

  /// Extend session (called when user is active)
  static Future<void> extendSession() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    bool? isLoggedIn = prefs.getBool(_isLoggedInKey);

    if (isLoggedIn == true) {
      // Extend session by 24 hours
      DateTime sessionExpiry = DateTime.now().add(Duration(hours: 24));
      await prefs.setString(_sessionExpiryKey, sessionExpiry.toIso8601String());
      await prefs.setString(_lastActivityKey, DateTime.now().toIso8601String());
    }
  }

  /// Check if session is about to expire (within 1 hour)
  static Future<bool> isSessionExpiringSoon() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    String? sessionExpiryStr = prefs.getString(_sessionExpiryKey);

    if (sessionExpiryStr != null) {
      DateTime sessionExpiry = DateTime.parse(sessionExpiryStr);
      DateTime oneHourFromNow = DateTime.now().add(Duration(hours: 1));
      return sessionExpiry.isBefore(oneHourFromNow);
    }

    return false;
  }
}
