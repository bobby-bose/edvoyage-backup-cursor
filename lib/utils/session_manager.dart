import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class SessionManager {
  static const String _emailKey = 'email';

  /// Save the email persistently
  static Future<void> storeEmail(String email) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_emailKey, email);
  }

  /// Retrieve the stored email (null if not set)
  static Future<String?> getStoredEmail() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_emailKey);
  }

  /// Clear stored email
  static Future<void> clearEmail() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_emailKey);
  }

  /// Fetch the full user data based on stored email
  static Future<Map<String, dynamic>?> fetchUserData() async {
    final email = await getStoredEmail();
    if (email == null) return null;

    // Use the exact URL with the email parameter
    final uri = Uri.parse(
        "https://bobbykbose37.pythonanywhere.com/api/v1/users/users/?email=$email");

    final response = await http.get(
      uri,
      headers: {
        "Content-Type": "application/json",
        // Add authorization header here if needed, e.g.
        // "Authorization": "Bearer YOUR_ACCESS_TOKEN",
      },
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return data; // Depends on API response structure
    } else {
      throw Exception(
          'Failed to fetch user data. Status: ${response.statusCode}');
    }
  }

  static Future<bool> isLoggedIn() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.containsKey(_emailKey);
  }
}
