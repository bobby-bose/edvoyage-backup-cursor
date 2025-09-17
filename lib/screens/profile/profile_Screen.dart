import 'dart:io';
import 'dart:convert'; // Added for jsonDecode
import 'dart:typed_data'; // Added for web image handling
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter/foundation.dart'; // Added for kIsWeb
import 'package:image_picker/image_picker.dart';
import 'package:path_provider/path_provider.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart'; // Added for Riverpod
import 'package:http/http.dart' as http; // Added for http
import 'package:frontend/utils/avatar.dart';
import 'package:frontend/utils/colors/colors.dart';
import 'package:frontend/utils/responsive.dart';
import 'package:frontend/_env/env.dart';
import 'package:frontend/screens/profile/profile_Tab/profile_feed.dart';
import 'package:frontend/screens/profile/profile_Tab/profile_about.dart';
import 'package:frontend/screens/profile/profile_Tab/profile_favorites.dart';
import 'package:frontend/screens/profile/profile_Tab/profile_application.dart';
import 'package:frontend/utils/constants.dart';
import 'package:frontend/utils/session_manager.dart'; // Added for session management

class UserProfile {
  final int id;
  final String userEmail;
  final String userUsername;
  final String userFirstName;
  final String userLastName;
  final String? phoneNumber;
  final String? dateOfBirth;
  final String? gender;
  final String? maritalStatus;
  final String? address;
  final String? city;
  final String? state;
  final String? country;
  final String? postalCode;
  final String? bio;
  final String? profilePicture;
  final String? coverPhoto;
  final bool emailNotifications;
  final bool pushNotifications;
  final bool smsNotifications;
  final bool isPhoneVerified;
  final bool isEmailVerified;
  final bool isProfileComplete;
  final int? age;
  final String fullName;
  final String? lastActive;
  final String createdAt;
  final String updatedAt;

  UserProfile({
    required this.id,
    required this.userEmail,
    required this.userUsername,
    required this.userFirstName,
    required this.userLastName,
    this.phoneNumber,
    this.dateOfBirth,
    this.gender,
    this.maritalStatus,
    this.address,
    this.city,
    this.state,
    this.country,
    this.postalCode,
    this.bio,
    this.profilePicture,
    this.coverPhoto,
    required this.emailNotifications,
    required this.pushNotifications,
    required this.smsNotifications,
    required this.isPhoneVerified,
    required this.isEmailVerified,
    required this.isProfileComplete,
    this.age,
    required this.fullName,
    this.lastActive,
    required this.createdAt,
    required this.updatedAt,
  });

  factory UserProfile.fromJson(Map<String, dynamic> json) => UserProfile(
        id: json['id'] ?? 0,
        userEmail: json['user_email'] ?? '',
        userUsername: json['user_username'] ?? '',
        userFirstName: json['user_first_name'] ?? '',
        userLastName: json['user_last_name'] ?? '',
        phoneNumber: json['phone_number'],
        dateOfBirth: json['date_of_birth'],
        gender: json['gender'],
        maritalStatus: json['marital_status'],
        address: json['address'],
        city: json['city'],
        state: json['state'],
        country: json['country'],
        postalCode: json['postal_code'],
        bio: json['bio'],
        profilePicture: json['profile_picture'],
        coverPhoto: json['cover_photo'],
        emailNotifications: json['email_notifications'] ?? true,
        pushNotifications: json['push_notifications'] ?? true,
        smsNotifications: json['sms_notifications'] ?? false,
        isPhoneVerified: json['is_phone_verified'] ?? false,
        isEmailVerified: json['is_email_verified'] ?? false,
        isProfileComplete: json['is_profile_complete'] ?? false,
        age: json['age'],
        fullName: json['full_name'] ?? '',
        lastActive: json['last_active'],
        createdAt: json['created_at'] ?? '',
        updatedAt: json['updated_at'] ?? '',
      );

  String get displayName =>
      fullName.isNotEmpty ? fullName : '$userFirstName $userLastName'.trim();
  String get avatarUrl {
    print('🔍 DEBUG: Profile picture value: $profilePicture');
    if (profilePicture != null && profilePicture!.isNotEmpty) {
      // If it's already a full URL, return as is
      if (profilePicture!.startsWith('http://') ||
          profilePicture!.startsWith('https://')) {
        print('🔍 DEBUG: Using full URL: $profilePicture');
        return profilePicture!;
      }
      // If it's a relative URL, convert to absolute URL
      if (profilePicture!.startsWith('/')) {
        final fullUrl = '${BaseUrl.baseUrlApi}${profilePicture}';
        print('🔍 DEBUG: Using relative URL converted to: $fullUrl');
        return fullUrl;
      }
      // If it's just a filename, construct the full URL
      final fullUrl = '${BaseUrl.baseUrlApi}/media/${profilePicture}';
      print('🔍 DEBUG: Using filename converted to: $fullUrl');
      return fullUrl;
    }
    print('🔍 DEBUG: Using fallback image');
    return 'https://www.topuniversities.com/sites/default/files/harvard_1.jpg';
  }
}

class ProfileState {
  final UserProfile? profile;
  final bool isLoading;
  final String? error;
  ProfileState({this.profile, required this.isLoading, this.error});
  ProfileState copyWith(
      {UserProfile? profile, bool? isLoading, String? error}) {
    return ProfileState(
      profile: profile ?? this.profile,
      isLoading: isLoading ?? this.isLoading,
      error: error,
    );
  }
}

class ProfileNotifier extends StateNotifier<ProfileState> {
  ProfileNotifier() : super(ProfileState(isLoading: false));

  Future<void> fetchProfile(String token) async {
    final userData = await SessionManager.fetchUserData();
    final phoneNumber = await SessionManager.getStoredEmail();
    state = state.copyWith(isLoading: true, error: null);
    try {
      var user = await SessionManager.fetchUserData();
      int userId = user?['id'] ?? 0;

      // Fetch real profile data from the backend API for current user
      final response = await http.get(
        Uri.parse('${BaseUrl.baseUrlApi}/api/v1/users/users/$userId/'),
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      );

      print('🔍 DEBUG: API Response Status: ${response.statusCode}');
      print('🔍 DEBUG: API Response Body: ${response.body}');

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        print('🔍 DEBUG: Parsed API data: $data');

        // Extract profile data from the user response
        final userData = data;
        final profileData = userData['profile'];

        if (profileData != null) {
          // Map the backend profile data to our UserProfile model
          final mappedProfileData = {
            'id': profileData['id'],
            'user_email': userData['email'],
            'user_username': userData['username'],
            'user_first_name': userData['first_name'] ?? '',
            'user_last_name': userData['last_name'] ?? '',
            'phone_number': profileData['phone_number'],
            'date_of_birth': profileData['date_of_birth'],
            'gender': profileData['gender'],
            'marital_status': profileData['marital_status'],
            'address': profileData['address'],
            'city': profileData['city'],
            'state': profileData['state'],
            'country': profileData['country'],
            'postal_code': profileData['postal_code'],
            'bio': profileData['bio'],
            'profile_picture': profileData['profile_picture'],
            'cover_photo': profileData['cover_photo'],
            'email_notifications': profileData['email_notifications'],
            'push_notifications': profileData['push_notifications'],
            'sms_notifications': profileData['sms_notifications'],
            'is_phone_verified': profileData['is_phone_verified'],
            'is_email_verified': profileData['is_email_verified'],
            'is_profile_complete': profileData['is_profile_complete'],
            'age': profileData['age'],
            'full_name': profileData['full_name'],
            'last_active': profileData['last_active'],
            'created_at': profileData['created_at'],
            'updated_at': profileData['updated_at'],
          };

          print('✅ DEBUG: Profile data mapped successfully for current user');
          print('🔍 DEBUG: Mapped profile data: $mappedProfileData');

          try {
            final userProfile = UserProfile.fromJson(mappedProfileData);
            print('✅ DEBUG: UserProfile created successfully');
            print('🔍 DEBUG: Profile display name: ${userProfile.displayName}');
            print('🔍 DEBUG: Profile picture: ${userProfile.profilePicture}');
            print('🔍 DEBUG: Avatar URL: ${userProfile.avatarUrl}');

            state = state.copyWith(profile: userProfile, isLoading: false);
            print('✅ DEBUG: Profile loaded successfully for current user');
          } catch (e) {
            print('❌ DEBUG: Error creating UserProfile: $e');
            state = state.copyWith(
                error: 'Error parsing profile data: $e', isLoading: false);
          }
        } else {
          print('❌ DEBUG: No profile data found for current user');

          final debugProfileData = {
            'id': userId,
            'user_email': phoneNumber,
            'user_username': userData?['username'] ?? 'user_$phoneNumber',
            'user_first_name': userData?['first_name'] ?? '',
            'user_last_name': userData?['last_name'] ?? '',
            'phone_number': phoneNumber ?? 'Unknown',
            'date_of_birth': null,
            'gender': '',
            'marital_status': '',
            'address': '',
            'city': '',
            'state': '',
            'country': '',
            'postal_code': '',
            'bio': '',
            'profile_picture': null,
            'cover_photo': null,
            'email_notifications': true,
            'push_notifications': true,
            'sms_notifications': false,
            'is_phone_verified': true,
            'is_email_verified': false,
            'is_profile_complete': false,
            'age': null,
            'full_name': userData?['full_name'] ?? 'User $phoneNumber',
            'last_active': DateTime.now().toIso8601String(),
            'created_at': DateTime.now().toIso8601String(),
            'updated_at': DateTime.now().toIso8601String(),
          };

          try {
            final debugProfile = UserProfile.fromJson(debugProfileData);
            print(
                '✅ DEBUG: Debug profile created successfully for current user');
            state = state.copyWith(profile: debugProfile, isLoading: false);
          } catch (e) {
            print('❌ DEBUG: Error creating debug profile: $e');
            state = state.copyWith(
                error: 'No profile data found', isLoading: false);
          }
        }
      } else {
        print(
            '❌ DEBUG: API request failed with status: ${response.statusCode}');

        // If user doesn't exist (404), create an empty profile for them to fill
        if (response.statusCode == 404) {
          final emptyProfileData = {
            'id': int.tryParse(userId.toString()) ?? 1, // Convert to int safely
            'user_email': userData?['email'] ?? '$phoneNumber@temp.com',
            'user_username': userData?['username'] ?? 'user_$phoneNumber',
            'user_first_name': userData?['first_name'] ?? '',
            'user_last_name': userData?['last_name'] ?? '',
            'phone_number': phoneNumber ?? 'Unknown',
            'date_of_birth': null,
            'gender': '',
            'marital_status': '',
            'address': '',
            'city': '',
            'state': '',
            'country': '',
            'postal_code': '',
            'bio': '',
            'profile_picture': null,
            'cover_photo': null,
            'email_notifications': true,
            'push_notifications': true,
            'sms_notifications': false,
            'is_phone_verified': true,
            'is_email_verified': false,
            'is_profile_complete': false,
            'age': null,
            'full_name': userData?['full_name'] ?? 'User $phoneNumber',
            'last_active': DateTime.now().toIso8601String(),
            'created_at': DateTime.now().toIso8601String(),
            'updated_at': DateTime.now().toIso8601String(),
          };

          try {
            final emptyProfile = UserProfile.fromJson(emptyProfileData);
            print('✅ DEBUG: Empty profile created successfully for new user');
            state = state.copyWith(profile: emptyProfile, isLoading: false);
          } catch (e) {
            print('❌ DEBUG: Error creating empty profile: $e');
            state = state.copyWith(
                error: 'Error creating profile: $e', isLoading: false);
          }
        } else {
          // For other errors, show the actual error
          state = state.copyWith(
              error: 'Failed to load profile: ${response.statusCode}',
              isLoading: false);
        }
      }
    } catch (e) {
      print('❌ DEBUG: Profile fetch error: $e');
      state = state.copyWith(
          error: 'Network or server error: $e', isLoading: false);
    }
  }

  Future<void> updateAvatar(String token, String filePath) async {
    try {
      var user = await SessionManager.fetchUserData();
      int userId = user?['id'] ?? 0;
      // Get current user ID from session

      print(
          '🔍 DEBUG: Updating avatar for current user ID: $userId with file: $filePath');

      // Create multipart request for file upload
      final request = http.MultipartRequest(
        'PUT',
        Uri.parse('${BaseUrl.baseUrlApi}/api/v1/users/profiles/$userId/'),
      );

      // Add headers
      request.headers['Content-Type'] = 'multipart/form-data';
      request.headers['Accept'] = 'application/json';

      // Note: We don't include email field when only updating profile picture
      // to avoid unique constraint errors
      print('🔍 DEBUG: Uploading profile picture only (no email field)');

      // Add the image file
      final file = await http.MultipartFile.fromPath(
        'profile_picture',
        filePath,
      );
      request.files.add(file);

      print('🔍 DEBUG: Sending multipart request to backend');
      final response = await request.send();
      final responseBody = await response.stream.bytesToString();

      print('🔍 DEBUG: Upload response status: ${response.statusCode}');
      print('🔍 DEBUG: Upload response body: $responseBody');

      if (response.statusCode == 200 || response.statusCode == 201) {
        final data = jsonDecode(responseBody);
        print('✅ DEBUG: Avatar updated successfully for current user');

        // Refresh the profile to get the updated data
        await fetchProfile(token);
      } else {
        print(
            '❌ DEBUG: Avatar upload failed with status: ${response.statusCode}');
        throw Exception('Failed to upload avatar: ${response.statusCode}');
      }
    } catch (e) {
      print('❌ DEBUG: Avatar update error: $e');
      rethrow;
    }
  }

  Future<void> updateProfile(String token, Map<String, dynamic> data) async {
    try {
      var user = await SessionManager.fetchUserData();
      int userId = user?['id'] ?? 0;
      if (userId == null || userId == 0) {
        throw Exception('User not authenticated. Please login again.');
      }

      print('🔍 DEBUG: Updating profile for current user ID: $userId');
      print('🔍 DEBUG: Update data: $data');

      // Send PUT request to update profile
      final response = await http.put(
        Uri.parse('${BaseUrl.baseUrlApi}/api/v1/users/profiles/$userId/'),
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: jsonEncode(data),
      );

      print('🔍 DEBUG: Update response status: ${response.statusCode}');
      print('🔍 DEBUG: Update response body: ${response.body}');

      if (response.statusCode == 200 || response.statusCode == 201) {
        final responseData = jsonDecode(response.body);
        print('✅ DEBUG: Profile updated successfully for current user');

        // Refresh the profile to get the updated data
        await fetchProfile(token);
      } else {
        print(
            '❌ DEBUG: Profile update failed with status: ${response.statusCode}');
        throw Exception('Failed to update profile: ${response.statusCode}');
      }
    } catch (e) {
      print('❌ DEBUG: Profile update error: $e');
      rethrow;
    }
  }
}

final profileProvider =
    StateNotifierProvider<ProfileNotifier, ProfileState>((ref) {
  return ProfileNotifier();
});

class ProfileScreen extends ConsumerStatefulWidget {
  const ProfileScreen({super.key});
  @override
  ConsumerState<ProfileScreen> createState() => _ProfileScreen();
}

class _ProfileScreen extends ConsumerState<ProfileScreen>
    with SingleTickerProviderStateMixin {
  TabController? _tabController;
  dynamic _image; // Changed from File? to dynamic to handle web
  ImageProvider? path;

  // Profile image upload state
  bool isUploadingImage = false;
  String? profileImageUrl;

  // Simple state for testing
  bool isLoading = true;
  String? error;
  UserProfile? profile;

  @override
  void initState() {
    super.initState();
    print('🔍 DEBUG: ProfileScreen initState called');
    _tabController = TabController(length: 4, vsync: this);
    print('🔍 DEBUG: About to call _loadProfile');
    _loadProfile();
    print('🔍 DEBUG: _loadProfile called');
  }

  Future<void> _loadProfile() async {
    var user = await SessionManager.fetchUserData();
    print('🔍 DEBUG: Fetched user data: $user');
    int userId = user!['results'][0]['id'];

    print('🔍 DEBUG: Loading profile for current user');
    print('🔍 DEBUG: User ID: $userId');
    print('🔍 DEBUG: User data: $user');
    print('🔍 DEBUG: This is the StatefulWidget implementation');

    setState(() {
      isLoading = true;
      error = null;
    });

    try {
      if (userId == null || userId == 0) {
        print('❌ DEBUG: No valid user ID found in session');
        setState(() {
          error = 'User not authenticated. Please login again.';
          isLoading = false;
        });
        return;
      }

      // Fetch real profile data from the backend API for current user
      final response = await http.get(
        Uri.parse('${BaseUrl.baseUrlApi}/api/v1/users/users/$userId/'),
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      );

      print('🔍 DEBUG: API Response Status: ${response.statusCode}');
      print('🔍 DEBUG: API Response Body: ${response.body}');

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        print('🔍 DEBUG: Parsed API data: $data');

        // Extract profile data from the user response
        final userData = data;
        final profileData = userData['profile'];

        if (profileData != null) {
          // Map the backend profile data to our UserProfile model
          final mappedProfileData = {
            'id': profileData['id'],
            'user_email': userData['email'],
            'user_username': userData['username'],
            'user_first_name': userData['first_name'] ?? '',
            'user_last_name': userData['last_name'] ?? '',
            'phone_number': profileData['phone_number'],
            'date_of_birth': profileData['date_of_birth'],
            'gender': profileData['gender'],
            'marital_status': profileData['marital_status'],
            'address': profileData['address'],
            'city': profileData['city'],
            'state': profileData['state'],
            'country': profileData['country'],
            'postal_code': profileData['postal_code'],
            'bio': profileData['bio'],
            'profile_picture': profileData['profile_picture'],
            'cover_photo': profileData['cover_photo'],
            'email_notifications': profileData['email_notifications'],
            'push_notifications': profileData['push_notifications'],
            'sms_notifications': profileData['sms_notifications'],
            'is_phone_verified': profileData['is_phone_verified'],
            'is_email_verified': profileData['is_email_verified'],
            'is_profile_complete': profileData['is_profile_complete'],
            'age': profileData['age'],
            'full_name': profileData['full_name'],
            'last_active': profileData['last_active'],
            'created_at': profileData['created_at'],
            'updated_at': profileData['updated_at'],
          };

          print('✅ DEBUG: Profile data mapped successfully for current user');
          print('🔍 DEBUG: Mapped profile data: $mappedProfileData');

          try {
            final userProfile = UserProfile.fromJson(mappedProfileData);
            print('✅ DEBUG: UserProfile created successfully');
            print('🔍 DEBUG: Profile display name: ${userProfile.displayName}');
            print('🔍 DEBUG: Profile picture: ${userProfile.profilePicture}');
            print('🔍 DEBUG: Avatar URL: ${userProfile.avatarUrl}');

            setState(() {
              profile = userProfile;
              isLoading = false;
            });
            print('✅ DEBUG: Profile loaded successfully for current user');
          } catch (e) {
            print('❌ DEBUG: Error creating UserProfile: $e');
            setState(() {
              error = 'Error parsing profile data: $e';
              isLoading = false;
            });
          }
        } else {
          print('❌ DEBUG: No profile data found for current user');
          var user = await SessionManager.fetchUserData();
          int userId = user?['id'] ?? 0;
          final email = await SessionManager.getStoredEmail();

          final debugProfileData = {
            'id': userId,
            'user_email': email,
            'user_username': email,
            'user_first_name': user?['first_name'] ?? '',
            'user_last_name': user?['last_name'] ?? '',
            'phone_number': user?['phone_number'] ?? 'Unknown',
            'date_of_birth': null,
            'gender': '',
            'marital_status': '',
            'address': '',
            'city': '',
            'state': '',
            'country': '',
            'postal_code': '',
            'bio': '',
            'profile_picture': null,
            'cover_photo': null,
            'email_notifications': true,
            'push_notifications': true,
            'sms_notifications': false,
            'is_phone_verified': true,
            'is_email_verified': false,
            'is_profile_complete': false,
            'age': null,
            'full_name': email,
            'last_active': DateTime.now().toIso8601String(),
            'created_at': DateTime.now().toIso8601String(),
            'updated_at': DateTime.now().toIso8601String(),
          };

          try {
            final debugProfile = UserProfile.fromJson(debugProfileData);
            print(
                '✅ DEBUG: Debug profile created successfully for current user');
            setState(() {
              profile = debugProfile;
              isLoading = false;
            });
          } catch (e) {
            print('❌ DEBUG: Error creating debug profile: $e');
            setState(() {
              error = 'No profile data found';
              isLoading = false;
            });
          }
        }
      } else {
        print(
            '❌ DEBUG: API request failed with status: ${response.statusCode}');

        // If user doesn't exist (404), create an empty profile for them to fill
        if (response.statusCode == 404) {
          print(
              '🔍 DEBUG: User profile not found (404), creating empty profile');
          var user = await SessionManager.fetchUserData();
          int userId = user?['id'] ?? 0;
          String? email = await SessionManager.getStoredEmail();
          final sessionUserData = await SessionManager.fetchUserData();

          final emptyProfileData = {
            'id': int.tryParse(userId.toString()) ?? 1, // Convert to int safely
            'user_email': email,
            'user_username': sessionUserData?['username'] ?? email,
            'user_first_name': sessionUserData?['first_name'] ?? '',
            'user_last_name': sessionUserData?['last_name'] ?? '',
            'phone_number': 'Unknown',
            'date_of_birth': null,
            'gender': '',
            'marital_status': '',
            'address': '',
            'city': '',
            'state': '',
            'country': '',
            'postal_code': '',
            'bio': '',
            'profile_picture': null,
            'cover_photo': null,
            'email_notifications': true,
            'push_notifications': true,
            'sms_notifications': false,
            'is_phone_verified': true,
            'is_email_verified': false,
            'is_profile_complete': false,
            'age': null,
            'full_name': sessionUserData?['full_name'] ?? email,
            'last_active': DateTime.now().toIso8601String(),
            'created_at': DateTime.now().toIso8601String(),
            'updated_at': DateTime.now().toIso8601String(),
          };

          try {
            final emptyProfile = UserProfile.fromJson(emptyProfileData);
            print('✅ DEBUG: Empty profile created successfully for new user');
            setState(() {
              profile = emptyProfile;
              isLoading = false;
            });
          } catch (e) {
            print('❌ DEBUG: Error creating empty profile: $e');
            setState(() {
              error = 'Error creating profile: $e';
              isLoading = false;
            });
          }
        } else {
          // For other errors, show the actual error
          setState(() {
            error = 'Failed to load profile: ${response.statusCode}';
            isLoading = false;
          });
        }
      }
    } catch (e) {
      print('❌ DEBUG: Profile fetch error: $e');
      setState(() {
        error = 'Network or server error: $e';
        isLoading = false;
      });
    }

    print('🔍 DEBUG: fetchProfile completed');
  }

  Future<void> _pickImage() async {
    try {
      setState(() {
        isUploadingImage = true;
      });

      final ImagePicker picker = ImagePicker();
      final XFile? image = await picker.pickImage(
        source: ImageSource.gallery,
        maxWidth: 512,
        maxHeight: 512,
        imageQuality: 85,
      );

      if (image != null) {
        setState(() {
          if (kIsWeb) {
            _image = image; // For web, store the XFile directly
          } else {
            _image = File(image.path); // For mobile, convert to File
          }
        });

        print('🔍 DEBUG: Starting profile image upload for current user');
        print('🔍 DEBUG: Image path: ${image.path}');
        print('🔍 DEBUG: Platform: ${kIsWeb ? 'Web' : 'Mobile'}');

        // Get current user ID from session
        final userId = await SessionManager.fetchUserData();

        if (userId == null || userId == 0) {
          throw Exception('User not authenticated. Please login again.');
        }

        // Create multipart request
        final request = http.MultipartRequest(
          'PUT',
          Uri.parse('${BaseUrl.baseUrlApi}/api/v1/users/profiles/$userId/'),
        );

        // Add headers
        request.headers['Content-Type'] = 'multipart/form-data';
        request.headers['Accept'] = 'application/json';

        // Note: We don't include email field when only updating profile picture
        // to avoid unique constraint errors
        print('🔍 DEBUG: Uploading profile picture only (no email field)');

        // Handle file upload differently for web vs mobile
        if (kIsWeb) {
          // For web, read the file as bytes
          final bytes = await image.readAsBytes();
          final multipartFile = http.MultipartFile.fromBytes(
            'profile_picture',
            bytes,
            filename: image.name,
          );
          request.files.add(multipartFile);
        } else {
          // For mobile, use the file path
          final file = await http.MultipartFile.fromPath(
            'profile_picture',
            image.path,
          );
          request.files.add(file);
        }

        print('🔍 DEBUG: Sending multipart request to backend');
        final response = await request.send();
        final responseBody = await response.stream.bytesToString();

        print('🔍 DEBUG: Upload response status: ${response.statusCode}');
        print('🔍 DEBUG: Upload response body: $responseBody');

        if (response.statusCode == 200 || response.statusCode == 201) {
          final data = jsonDecode(responseBody);
          print('✅ DEBUG: Avatar updated successfully for User ID=1');
          print('🔍 DEBUG: Response data: $data');

          // Refresh the profile to get the updated image URL
          await _loadProfile();

          // Show success message
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('Profile picture updated successfully!'),
              backgroundColor: Colors.green,
            ),
          );
        } else {
          print(
              '❌ DEBUG: Avatar upload failed with status: ${response.statusCode}');
          throw Exception('Failed to upload avatar: ${response.statusCode}');
        }
      }
    } catch (e) {
      print('❌ DEBUG: Image picker error: $e');
      // Show error to user
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Failed to upload image: $e'),
          backgroundColor: Colors.red,
        ),
      );
    } finally {
      setState(() {
        isUploadingImage = false;
      });
    }
  }

  Measurements? size;

  @override
  Widget build(BuildContext context) {
    size = Measurements(MediaQuery.of(context).size);

    // Simple debug print to see if build is working
    print(
        '🔍 DEBUG: Profile screen build - isLoading: $isLoading, has profile: ${profile != null}');
    if (profile != null) {
      print("the full profile data is ${profile}");
      print('🔍 DEBUG: Profile picture URL: ${profile!.profilePicture}');
      print('🔍 DEBUG: Avatar URL: ${profile!.avatarUrl}');
    }

    return PopScope(
        canPop: false,
        onPopInvokedWithResult: (didPop, result) {
          if (!didPop) {
            SystemNavigator.pop(); // exit the app
          }
        },
        child: Scaffold(
          backgroundColor: Colors.white,
          appBar: AppBar(
            leading: IconButton(
              onPressed: () {
                Navigator.pop(context);
              },
              icon: const Icon(Icons.arrow_back),
            ),
            backgroundColor: const Color.fromARGB(255, 255, 255, 255),
            elevation: 3,
            centerTitle: true,
            title: SizedBox(
              height: 250,
              width: 200,
              child: Image.asset(edvoyagelogo1),
            ),
          ),
          body: isLoading
              ? const Center(child: CircularProgressIndicator())
              : error != null
                  ? Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Text(error!, style: TextStyle(color: Colors.red)),
                          SizedBox(height: 16),
                          ElevatedButton(
                            onPressed: _loadProfile,
                            child: Text('Retry'),
                          ),
                          SizedBox(height: 16),
                          // Show a simple profile for testing
                          Text('Showing test profile for debugging'),
                          Text('User: user_7012085349'),
                          Text('Phone: 7012085349'),
                        ],
                      ),
                    )
                  : SafeArea(
                      child: SizedBox.expand(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.center,
                          children: [
                            // ---------- PROFILE HEADER ----------
                            Stack(
                              children: [
                                Container(
                                  height: size?.hp(24),
                                  width: double.infinity,
                                  color: thirdColor,
                                ),
                                Container(
                                  height: size?.hp(14),
                                  decoration:
                                      BoxDecoration(color: primaryColor),
                                ),
                                Column(
                                  children: [
                                    SizedBox(height: size?.hp(5)),
                                    Container(
                                      alignment: const Alignment(-0.8, 0),
                                      child: Column(
                                        crossAxisAlignment:
                                            CrossAxisAlignment.center,
                                        children: [
                                          Stack(
                                            children: [
                                              CircleAvatar(
                                                radius: 60,
                                                backgroundColor:
                                                    Colors.grey[300],
                                                backgroundImage: profile != null
                                                    ? NetworkImage(
                                                        profile!.avatarUrl,
                                                        headers: {
                                                          'User-Agent':
                                                              'Flutter App'
                                                        },
                                                      )
                                                    : null,
                                                onBackgroundImageError:
                                                    (exception, stackTrace) {
                                                  print(
                                                      '❌ DEBUG: Failed to load profile image: $exception');
                                                },
                                                child:
                                                    profile?.profilePicture ==
                                                                null ||
                                                            profile!
                                                                .profilePicture!
                                                                .isEmpty
                                                        ? Icon(Icons.person,
                                                            size: 60,
                                                            color: Colors
                                                                .grey[600])
                                                        : null,
                                              ),
                                              Positioned(
                                                top: 70,
                                                left: 85,
                                                child: Container(
                                                  width: size?.wp(8),
                                                  height: size?.hp(8),
                                                  decoration: BoxDecoration(
                                                    color: thirdColor,
                                                    shape: BoxShape.circle,
                                                    boxShadow: [
                                                      BoxShadow(
                                                          color: Colors.grey,
                                                          blurRadius: 5),
                                                    ],
                                                  ),
                                                  child: isUploadingImage
                                                      ? Center(
                                                          child: SizedBox(
                                                            width: 16,
                                                            height: 16,
                                                            child:
                                                                CircularProgressIndicator(
                                                              strokeWidth: 2,
                                                              valueColor:
                                                                  AlwaysStoppedAnimation<
                                                                          Color>(
                                                                      Colors
                                                                          .black),
                                                            ),
                                                          ),
                                                        )
                                                      : TextButton(
                                                          onPressed: _pickImage,
                                                          child: const Icon(
                                                            Icons
                                                                .camera_alt_outlined,
                                                            size: 18,
                                                            color: Colors.black,
                                                          ),
                                                        ),
                                                ),
                                              ),
                                            ],
                                          ),
                                          vGap(5),
                                          Text(
                                            profile?.displayName ?? 'User',
                                            style: const TextStyle(
                                              fontFamily: 'Poppins',
                                              fontWeight: FontWeight.w500,
                                              fontSize: 15,
                                            ),
                                          ),
                                        ],
                                      ),
                                    ),
                                  ],
                                ),
                              ],
                            ),

                            // ---------- TABBAR ----------
                            Container(
                              color: whiteColor,
                              child: TabBar(
                                controller: _tabController,
                                labelPadding: EdgeInsets.zero,
                                unselectedLabelColor: Colors.grey,
                                labelColor: secondaryColor,
                                indicatorColor: Cprimary,
                                labelStyle: Theme.of(context)
                                    .textTheme
                                    .titleSmall!
                                    .copyWith(
                                      fontSize: 15.0,
                                      fontWeight: FontWeight.w500,
                                      color: Colors.orange,
                                    ),
                                unselectedLabelStyle: Theme.of(context)
                                    .textTheme
                                    .titleSmall!
                                    .copyWith(
                                      fontSize: 14.0,
                                      fontWeight: FontWeight.w500,
                                      color: Colors.grey[200],
                                    ),
                                indicatorSize: TabBarIndicatorSize.tab,
                                tabs: const [
                                  Tab(child: Text('Feed')),
                                  Tab(child: Text('About')),
                                  Tab(child: Text('Favourites')),
                                  Tab(child: Text('Applications')),
                                ],
                              ),
                            ),

                            // ---------- TABBAR VIEW ----------
                            Expanded(
                              child: TabBarView(
                                controller: _tabController,
                                children: const [
                                  ProfileFeed(),
                                  ProfileAbout(),
                                  ProfileFevourites(),
                                  ProfileApplication(),
                                ],
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
        ));
  }
}
