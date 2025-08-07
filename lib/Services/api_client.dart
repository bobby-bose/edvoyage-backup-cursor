import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;
import '../_env/env.dart';
import '../utils/session_manager.dart';

class ApiClient {
  static const String baseUrl = BaseUrl.baseUrl;

  /// Make a GET request with user session headers
  static Future<http.Response> get(String endpoint) async {
    Map<String, String> headers = await SessionManager.getApiHeaders();

    return await http.get(
      Uri.parse('$baseUrl$endpoint'),
      headers: headers,
    );
  }

  /// Make a POST request with user session headers
  static Future<http.Response> post(
      String endpoint, Map<String, dynamic> data) async {
    Map<String, String> headers = await SessionManager.getApiHeaders();

    return await http.post(
      Uri.parse('$baseUrl$endpoint'),
      headers: headers,
      body: jsonEncode(data),
    );
  }

  /// Make a PUT request with user session headers
  static Future<http.Response> put(
      String endpoint, Map<String, dynamic> data) async {
    Map<String, String> headers = await SessionManager.getApiHeaders();

    return await http.put(
      Uri.parse('$baseUrl$endpoint'),
      headers: headers,
      body: jsonEncode(data),
    );
  }

  /// Make a DELETE request with user session headers
  static Future<http.Response> delete(String endpoint) async {
    Map<String, String> headers = await SessionManager.getApiHeaders();

    return await http.delete(
      Uri.parse('$baseUrl$endpoint'),
      headers: headers,
    );
  }

  /// Make a PATCH request with user session headers
  static Future<http.Response> patch(
      String endpoint, Map<String, dynamic> data) async {
    Map<String, String> headers = await SessionManager.getApiHeaders();

    return await http.patch(
      Uri.parse('$baseUrl$endpoint'),
      headers: headers,
      body: jsonEncode(data),
    );
  }

  /// Add user ID to request data
  static Future<Map<String, dynamic>> addUserIdToData(
      Map<String, dynamic> data) async {
    return await SessionManager.addUserIdToRequest(data);
  }

  /// Check if user is authenticated
  static Future<bool> isAuthenticated() async {
    return await SessionManager.isLoggedIn();
  }

  /// Get current user ID
  static Future<String?> getCurrentUserId() async {
    return await SessionManager.getUserId();
  }

  /// Handle API response and check for authentication errors
  static Map<String, dynamic> handleResponse(http.Response response) {
    if (response.statusCode == 401) {
      // Unauthorized - user needs to login again
      throw Exception('Authentication required');
    }

    if (response.statusCode >= 200 && response.statusCode < 300) {
      return jsonDecode(response.body);
    } else {
      throw Exception('API Error: ${response.statusCode} - ${response.body}');
    }
  }

  /// Make authenticated request with error handling
  static Future<Map<String, dynamic>> authenticatedRequest(
    String method,
    String endpoint, {
    Map<String, dynamic>? data,
  }) async {
    try {
      http.Response response;

      switch (method.toUpperCase()) {
        case 'GET':
          response = await get(endpoint);
          break;
        case 'POST':
          response = await post(endpoint, data ?? {});
          break;
        case 'PUT':
          response = await put(endpoint, data ?? {});
          break;
        case 'DELETE':
          response = await delete(endpoint);
          break;
        case 'PATCH':
          response = await patch(endpoint, data ?? {});
          break;
        default:
          throw Exception('Unsupported HTTP method: $method');
      }

      return handleResponse(response);
    } catch (e) {
      if (e.toString().contains('Authentication required')) {
        // Handle authentication error
        throw Exception('Please login again');
      }
      rethrow;
    }
  }
}
