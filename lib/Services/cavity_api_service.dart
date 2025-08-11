import 'dart:convert';
import 'package:http/http.dart' as http;
import '../_env/env.dart';
import '../utils/session_manager.dart';

class CavityApiService {
  static String get baseUrl => BaseUrl.baseUrlApi + '/api/v1/cavity';

  /// Get API headers with authentication
  static Future<Map<String, String>> _getHeaders() async {
    print('🔍 DEBUG: Starting _getHeaders method');
    print('🔍 DEBUG: Creating basic headers map');
    Map<String, String> headers = {
      'Content-Type': 'application/json',
    };

    print('🔍 DEBUG: Final headers: $headers');
    print('🔍 DEBUG: Returning headers');
    return headers;
  }

  /// Fetch posts by year
  static Future<List<Map<String, dynamic>>> getPostsByYear(String year) async {
    print('🔍 DEBUG: Starting getPostsByYear method');
    print('🔍 DEBUG: Year parameter: $year');

    try {
      print('🔍 DEBUG: About to call _getHeaders()');
      final headers = await _getHeaders();
      print('🔍 DEBUG: Headers received: $headers');

      print('🔍 DEBUG: About to construct URL');
      final url = '$baseUrl/api/posts/?year=$year';
      print('🔍 DEBUG: Constructed URL: $url');

      print('🔍 DEBUG: About to make HTTP GET request');
      final response = await http.get(
        Uri.parse(url),
        headers: headers,
      );
      print('🔍 DEBUG: HTTP request completed');

      print('🔍 DEBUG: Response status code: ${response.statusCode}');
      print('🔍 DEBUG: Response headers: ${response.headers}');
      print('🔍 DEBUG: Response body POSTTTTTSSS: ${response.body}');

      if (response.statusCode == 200) {
        print('🔍 DEBUG: Status code is 200, processing response');
        print('🔍 DEBUG: About to decode JSON');
        final data = jsonDecode(response.body);
        print('🔍 DEBUG: JSON decoded successfully: $data');

        if (data['results'] != null) {
          print('🔍 DEBUG: Found results in response');
          final results = List<Map<String, dynamic>>.from(data['results']);
          print('🔍 DEBUG: Converted to List, count: ${results.length}');
          return results;
        } else if (data is List) {
          print('🔍 DEBUG: Response is directly a List');
          final results = List<Map<String, dynamic>>.from(data);
          print('🔍 DEBUG: Converted List, count: ${results.length}');
          return results;
        } else {
          print('🔍 DEBUG: No results found in response');
        }
      } else if (response.statusCode == 401) {
        print('🔍 DEBUG: Authentication required (401)');
        return [];
      } else {
        print('🔍 DEBUG: Unexpected status code: ${response.statusCode}');
      }

      print('🔍 DEBUG: Returning empty list');
      return [];
    } catch (e) {
      print('❌ ERROR in getPostsByYear: $e');
      print('❌ ERROR type: ${e.runtimeType}');
      print('❌ ERROR stack trace: ${StackTrace.current}');
      return [];
    }
  }

  /// Fetch all users
  static Future<List<Map<String, dynamic>>> getUsers() async {
    try {
      final headers = await _getHeaders();
      final response = await http.get(
        Uri.parse('$baseUrl/users/'),
        headers: headers,
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        if (data['results'] != null) {
          return List<Map<String, dynamic>>.from(data['results']);
        }
      }

      return [];
    } catch (e) {
      print('Error fetching users: $e');
      return [];
    }
  }

  /// Like a post
  static Future<bool> likePost(String postId) async {
    try {
      print('🔍 DEBUG: Starting likePost method');
      print('🔍 DEBUG: Post ID: $postId');

      final headers = await _getHeaders();
      print('🔍 DEBUG: Headers: $headers');

      print('🔍 DEBUG: About to make HTTP POST request');
      final response = await http.post(
        Uri.parse('$baseUrl/posts/$postId/like/'),
        headers: headers,
      );

      print('🔍 DEBUG: HTTP POST request completed');
      print('🔍 DEBUG: Like post response - Status: ${response.statusCode}');
      print('🔍 DEBUG: Like post response - Headers: ${response.headers}');
      print('🔍 DEBUG: Like post response - Body: ${response.body}');
      print(
          '🔍 DEBUG: Like post response - Reason phrase: ${response.reasonPhrase}');

      if (response.statusCode == 200 || response.statusCode == 201) {
        print('✅ Post liked successfully!');
        print('✅ Response status: ${response.statusCode}');
        print('✅ Response body: ${response.body}');
        return true;
      } else {
        print('❌ Failed to like post. Status: ${response.statusCode}');
        print('❌ Response reason phrase: ${response.reasonPhrase}');
        print('❌ Response body: ${response.body}');
        print('❌ Response headers: ${response.headers}');

        // Try to parse error response
        try {
          final errorData = jsonDecode(response.body);
          print('❌ Parsed error data: $errorData');
        } catch (e) {
          print('❌ Could not parse error response as JSON: $e');
        }

        return false;
      }
    } catch (e) {
      print('❌ Error liking post: $e');
      print('❌ Error type: ${e.runtimeType}');
      print('❌ Error stack trace: ${StackTrace.current}');

      // Check if it's a network error
      if (e.toString().contains('Failed to fetch')) {
        print('❌ This appears to be a network connectivity issue');
        print('❌ Check if the backend server is running on 192.168.137.1:8000');
      }

      return false;
    }
  }

  /// Unlike a post
  static Future<bool> unlikePost(String postId) async {
    try {
      print('🔍 DEBUG: Starting unlikePost method');
      print('🔍 DEBUG: Post ID: $postId');

      final headers = await _getHeaders();
      print('🔍 DEBUG: Headers: $headers');

      print('🔍 DEBUG: About to make HTTP DELETE request');
      final response = await http.delete(
        Uri.parse('$baseUrl/posts/$postId/like/'),
        headers: headers,
      );

      print('🔍 DEBUG: HTTP DELETE request completed');
      print('🔍 DEBUG: Unlike post response - Status: ${response.statusCode}');
      print('🔍 DEBUG: Unlike post response - Headers: ${response.headers}');
      print('🔍 DEBUG: Unlike post response - Body: ${response.body}');
      print(
          '🔍 DEBUG: Unlike post response - Reason phrase: ${response.reasonPhrase}');

      if (response.statusCode == 200 || response.statusCode == 204) {
        print('✅ Post unliked successfully!');
        print('✅ Response status: ${response.statusCode}');
        print('✅ Response body: ${response.body}');
        return true;
      } else {
        print('❌ Failed to unlike post. Status: ${response.statusCode}');
        print('❌ Response reason phrase: ${response.reasonPhrase}');
        print('❌ Response body: ${response.body}');
        print('❌ Response headers: ${response.headers}');

        // Try to parse error response
        try {
          final errorData = jsonDecode(response.body);
          print('❌ Parsed error data: $errorData');
        } catch (e) {
          print('❌ Could not parse error response as JSON: $e');
        }

        return false;
      }
    } catch (e) {
      print('❌ Error unliking post: $e');
      print('❌ Error type: ${e.runtimeType}');
      print('❌ Error stack trace: ${StackTrace.current}');

      // Check if it's a network error
      if (e.toString().contains('Failed to fetch')) {
        print('❌ This appears to be a network connectivity issue');
        print('❌ Check if the backend server is running on 192.168.137.1:8000');
      }

      return false;
    }
  }

  /// Like a post and return response data
  static Future<Map<String, dynamic>?> likePostWithResponse(
      String postId) async {
    try {
      print('🔍 DEBUG: Starting likePostWithResponse method');
      print('🔍 DEBUG: Post ID: $postId');

      final headers = await _getHeaders();
      print('🔍 DEBUG: Headers: $headers');

      print('🔍 DEBUG: About to make HTTP POST request');
      final response = await http.post(
        Uri.parse('$baseUrl/posts/$postId/like/'),
        headers: headers,
      );

      print('🔍 DEBUG: HTTP POST request completed');
      print('🔍 DEBUG: Like post response - Status: ${response.statusCode}');
      print('🔍 DEBUG: Like post response - Headers: ${response.headers}');
      print('🔍 DEBUG: Like post response - Body: ${response.body}');
      print(
          '🔍 DEBUG: Like post response - Reason phrase: ${response.reasonPhrase}');

      if (response.statusCode == 200 || response.statusCode == 201) {
        print('✅ Post liked successfully!');
        print('✅ Response status: ${response.statusCode}');
        print('✅ Response body: ${response.body}');

        // Parse response data
        try {
          final responseData = jsonDecode(response.body);
          print('✅ Parsed response data: $responseData');
          return responseData;
        } catch (e) {
          print('❌ Error parsing response data: $e');
          return null;
        }
      } else {
        print('❌ Failed to like post. Status: ${response.statusCode}');
        print('❌ Response reason phrase: ${response.reasonPhrase}');
        print('❌ Response body: ${response.body}');
        print('❌ Response headers: ${response.headers}');

        // Try to parse error response
        try {
          final errorData = jsonDecode(response.body);
          print('❌ Parsed error data: $errorData');
        } catch (e) {
          print('❌ Could not parse error response as JSON: $e');
        }

        return null;
      }
    } catch (e) {
      print('❌ Error liking post: $e');
      print('❌ Error type: ${e.runtimeType}');
      print('❌ Error stack trace: ${StackTrace.current}');

      // Check if it's a network error
      if (e.toString().contains('Failed to fetch')) {
        print('❌ This appears to be a network connectivity issue');
        print('❌ Check if the backend server is running on 192.168.137.1:8000');
      }

      return null;
    }
  }

  /// Unlike a post and return response data
  static Future<Map<String, dynamic>?> unlikePostWithResponse(
      String postId) async {
    try {
      print('🔍 DEBUG: Starting unlikePostWithResponse method');
      print('🔍 DEBUG: Post ID: $postId');

      final headers = await _getHeaders();
      print('🔍 DEBUG: Headers: $headers');

      print('🔍 DEBUG: About to make HTTP DELETE request');
      final response = await http.delete(
        Uri.parse('$baseUrl/posts/$postId/like/'),
        headers: headers,
      );

      print('🔍 DEBUG: HTTP DELETE request completed');
      print('🔍 DEBUG: Unlike post response - Status: ${response.statusCode}');
      print('🔍 DEBUG: Unlike post response - Headers: ${response.headers}');
      print('🔍 DEBUG: Unlike post response - Body: ${response.body}');
      print(
          '🔍 DEBUG: Unlike post response - Reason phrase: ${response.reasonPhrase}');

      if (response.statusCode == 200 || response.statusCode == 204) {
        print('✅ Post unliked successfully!');
        print('✅ Response status: ${response.statusCode}');
        print('✅ Response body: ${response.body}');

        // Parse response data
        try {
          final responseData = jsonDecode(response.body);
          print('✅ Parsed response data: $responseData');
          return responseData;
        } catch (e) {
          print('❌ Error parsing response data: $e');
          return null;
        }
      } else {
        print('❌ Failed to unlike post. Status: ${response.statusCode}');
        print('❌ Response reason phrase: ${response.reasonPhrase}');
        print('❌ Response body: ${response.body}');
        print('❌ Response headers: ${response.headers}');

        // Try to parse error response
        try {
          final errorData = jsonDecode(response.body);
          print('❌ Parsed error data: $errorData');
        } catch (e) {
          print('❌ Could not parse error response as JSON: $e');
        }

        return null;
      }
    } catch (e) {
      print('❌ Error unliking post: $e');
      print('❌ Error type: ${e.runtimeType}');
      print('❌ Error stack trace: ${StackTrace.current}');

      // Check if it's a network error
      if (e.toString().contains('Failed to fetch')) {
        print('❌ This appears to be a network connectivity issue');
        print('❌ Check if the backend server is running on 192.168.137.1:8000');
      }

      return null;
    }
  }

  /// Add comment to post
  static Future<bool> addComment(
      String postId, String content, String email) async {
    try {
      print('🔍 DEBUG: Starting addComment method');
      print('🔍 DEBUG: Post ID: $postId');
      print('🔍 DEBUG: Content: $content');

      final requestBody = {
        'post': postId,
        'content': content,
        'email': email, // Include email in the request body
      };

      print('🔍 DEBUG: Creating comment with data: $requestBody');
      print('🔍 DEBUG: Base URL: $baseUrl');
      print('🔍 DEBUG: Full URL: $baseUrl/comments/create/');

      // Log the exact JSON being sent
      final jsonBody = jsonEncode(requestBody);
      print('🔍 DEBUG: JSON body being sent: $jsonBody');

      print('🔍 DEBUG: About to make HTTP POST request');
      final response = await http.post(
        Uri.parse('$baseUrl/api/comments/create/'),
        headers: {
          "Content-Type": "application/json",
          "Accept": "application/json",
        },
        body: jsonBody,
      );

      print('🔍 DEBUG: HTTP POST request completed');
      print('🔍 DEBUG: Add comment response - Status: ${response.statusCode}');
      print('🔍 DEBUG: Add comment response - Headers: ${response.headers}');
      print('🔍 DEBUG: Add comment response - Body: ${response.body}');
      print(
          '🔍 DEBUG: Add comment response - Reason phrase: ${response.reasonPhrase}');

      if (response.statusCode == 200 || response.statusCode == 201) {
        print('✅ Comment added successfully!');
        print('✅ Response status: ${response.statusCode}');
        print('✅ Response body: ${response.body}');
        return true;
      } else {
        print('❌ Failed to add comment. Status: ${response.statusCode}');
        print('❌ Response reason phrase: ${response.reasonPhrase}');
        print('❌ Response body: ${response.body}');
        print('❌ Response headers: ${response.headers}');

        // Try to parse error response
        try {
          final errorData = jsonDecode(response.body);
          print('❌ Parsed error data: $errorData');
        } catch (e) {
          print('❌ Could not parse error response as JSON: $e');
        }

        return false;
      }
    } catch (e) {
      print('❌ Error adding comment: $e');
      print('❌ Error type: ${e.runtimeType}');
      print('❌ Error stack trace: ${StackTrace.current}');

      // Check if it's a network error
      if (e.toString().contains('Failed to fetch')) {
        print('❌ This appears to be a network connectivity issue');
        print('❌ Check if the backend server is running on 192.168.137.1:8000');
      }

      return false;
    }
  }

  /// Share a post
  static Future<bool> sharePost(String postId, String platform) async {
    try {
      final headers = await _getHeaders();
      final response = await http.post(
        Uri.parse('$baseUrl/posts/$postId/share/'),
        headers: headers,
        body: jsonEncode({
          'platform': platform,
        }),
      );

      return response.statusCode == 200 || response.statusCode == 201;
    } catch (e) {
      print('Error sharing post: $e');
      return false;
    }
  }

  /// Test API connectivity
  static Future<bool> testApiConnection() async {
    print('🔍 DEBUG: Starting testApiConnection method');
    print('🔍 DEBUG: Base URL: $baseUrl');

    try {
      print('🔍 DEBUG: About to construct test URL');
      final testUrl = '$baseUrl/posts/';
      print('🔍 DEBUG: Test URL constructed: $testUrl');

      print('🔍 DEBUG: About to create headers for test');
      final headers = {'Content-Type': 'application/json'};
      print('🔍 DEBUG: Test headers created: $headers');

      print('🔍 DEBUG: About to make HTTP GET request for test');
      final response = await http.get(
        Uri.parse(testUrl),
        headers: headers,
      );
      print('🔍 DEBUG: Test HTTP request completed');

      print('🔍 DEBUG: Test response status code: ${response.statusCode}');
      print('🔍 DEBUG: Test response headers: ${response.headers}');
      print('🔍 DEBUG: Test response body: ${response.body}');

      print('🔍 DEBUG: Checking if status code is 200');
      final isSuccess = response.statusCode == 200;
      print('🔍 DEBUG: Test result: $isSuccess');

      return isSuccess;
    } catch (e) {
      print('❌ ERROR in testApiConnection: $e');
      print('❌ ERROR type: ${e.runtimeType}');
      print('❌ ERROR stack trace: ${StackTrace.current}');
      return false;
    }
  }

  /// Create a new post
  static Future<bool> createPost(String content,
      {bool isAnonymous = false, required String year}) async {
    try {
      print('🔍 DEBUG: Starting createPost method');
      print('🔍 DEBUG: Content: $content');
      print('🔍 DEBUG: Year: $year');
      print('🔍 DEBUG: IsAnonymous: $isAnonymous');

      final headers = await _getHeaders();
      print('🔍 DEBUG: Headers: $headers');

      // Get current user ID
      print('🔍 DEBUG: About to get current user ID');
      Map<String, dynamic>? currentUserId =
          await SessionManager.fetchUserData();
      if (currentUserId != null) {
        currentUserId = currentUserId['id'];
      }
      print('🔍 DEBUG: Current user ID: $currentUserId');

      // Handle case where user is not logged in
      if (currentUserId == null || currentUserId.isEmpty) {
        print(
            '⚠️ WARNING: No user ID available, post will be created with default user');
        // For now, we'll still try to create the post and let backend handle it
        // In production, you might want to redirect to login
      }

      // Create the request body with user_id
      final requestBody = {
        'content': content,
        'year': year,
        'is_anonymous': isAnonymous,
        'user_id': currentUserId, // Add user_id to request (can be null)
      };

      print('🔍 DEBUG: Creating post with data: $requestBody');
      print('🔍 DEBUG: Base URL: $baseUrl');
      print('🔍 DEBUG: Full URL: $baseUrl/posts/');

      // Log the exact JSON being sent
      final jsonBody = jsonEncode(requestBody);
      print('🔍 DEBUG: JSON body being sent: $jsonBody');

      print('🔍 DEBUG: About to make HTTP POST request');
      final response = await http.post(
        Uri.parse('$baseUrl/posts/'),
        headers: headers,
        body: jsonBody,
      );

      print('🔍 DEBUG: HTTP POST request completed');
      print('🔍 DEBUG: Create post response - Status: ${response.statusCode}');
      print('🔍 DEBUG: Create post response - Headers: ${response.headers}');
      print('🔍 DEBUG: Create post response - Body: ${response.body}');
      print(
          '🔍 DEBUG: Create post response - Reason phrase: ${response.reasonPhrase}');

      if (response.statusCode == 200 || response.statusCode == 201) {
        print('✅ Post created successfully!');
        print('✅ Response status: ${response.statusCode}');
        print('✅ Response body: ${response.body}');
        return true;
      } else {
        print('❌ Failed to create post. Status: ${response.statusCode}');
        print('❌ Response reason phrase: ${response.reasonPhrase}');
        print('❌ Response body: ${response.body}');
        print('❌ Response headers: ${response.headers}');

        // Try to parse error response
        try {
          final errorData = jsonDecode(response.body);
          print('❌ Parsed error data: $errorData');
        } catch (e) {
          print('❌ Could not parse error response as JSON: $e');
        }

        return false;
      }
    } catch (e) {
      print('❌ Error creating post: $e');
      print('❌ Error type: ${e.runtimeType}');
      print('❌ Error stack trace: ${StackTrace.current}');

      // Check if it's a network error
      if (e.toString().contains('Failed to fetch')) {
        print('❌ This appears to be a network connectivity issue');
        print('❌ Check if the backend server is running on 192.168.137.1:8000');
      }

      return false;
    }
  }
}
