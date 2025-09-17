import 'dart:convert';
import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:frontend/utils/colors/colors.dart';

class ChatScreen extends StatefulWidget {
  const ChatScreen({super.key});

  @override
  _ChatScreenState createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  List<Map<String, dynamic>> allContacts = [];
  List<Map<String, dynamic>> filteredContacts = [];
  TextEditingController searchController = TextEditingController();
  bool isLoading = true;
  bool isSearching = false;
  Timer? _debounceTimer;

  @override
  void initState() {
    super.initState();
    _loadContacts();
    searchController.addListener(_onSearchChanged);
  }

  @override
  void dispose() {
    searchController.removeListener(_onSearchChanged);
    searchController.dispose();
    _debounceTimer?.cancel();
    super.dispose();
  }

  /// Load contacts from JSON file
  Future<void> _loadContacts() async {
    try {
      setState(() {
        isLoading = true;
      });

      final String response =
          await rootBundle.loadString('lib/screens/chat/data.json');
      final List<dynamic> jsonData = json.decode(response);

      setState(() {
        allContacts = List<Map<String, dynamic>>.from(jsonData);
        filteredContacts = List.from(allContacts);
        isLoading = false;
      });
    } catch (e) {
      print('Error loading chat contacts: $e');
      setState(() {
        isLoading = false;
      });
    }
  }

  /// Debounced search functionality
  void _onSearchChanged() {
    if (_debounceTimer?.isActive ?? false) _debounceTimer!.cancel();
    _debounceTimer = Timer(Duration(milliseconds: 300), () {
      _filterContacts();
    });
  }

  /// Filter contacts based on search query
  void _filterContacts() {
    final query = searchController.text.toLowerCase().trim();

    setState(() {
      isSearching = query.isNotEmpty;

      if (query.isEmpty) {
        filteredContacts = List.from(allContacts);
      } else {
        filteredContacts = allContacts.where((contact) {
          final name = contact['name']?.toString().toLowerCase() ?? '';
          final role = contact['role']?.toString().toLowerCase() ?? '';
          final institution =
              contact['institution']?.toString().toLowerCase() ?? '';

          return name.contains(query) ||
              role.contains(query) ||
              institution.contains(query);
        }).toList();
      }
    });
  }

  /// Clear search and show all contacts
  void _clearSearch() {
    searchController.clear();
    setState(() {
      filteredContacts = List.from(allContacts);
      isSearching = false;
    });
  }

  /// Handle add contact action
  void _addContact(Map<String, dynamic> contact) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('Added ${contact['name']} to contacts'),
        backgroundColor: primaryColor,
        duration: Duration(seconds: 2),
      ),
    );
  }

  /// Build search header with text field and cancel button
  Widget _buildSearchHeader() {
    return Container(
      padding: EdgeInsets.symmetric(horizontal: 20, vertical: 15),
      decoration: BoxDecoration(
        color: whiteColor,
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.05),
            blurRadius: 10,
            offset: Offset(0, 2),
          ),
        ],
      ),
      child: Row(
        children: [
          // Search Field
          Expanded(
            child: Container(
              height: 45,
              decoration: BoxDecoration(
                color: grey1.withValues(alpha: 0.1),
                borderRadius: BorderRadius.circular(20),
              ),
              child: TextField(
                controller: searchController,
                decoration: InputDecoration(
                  hintText: 'Search by name...',
                  hintStyle: TextStyle(
                    fontFamily: 'Poppins',
                    fontSize: 14,
                    color: grey3,
                  ),
                  prefixIcon: Icon(
                    Icons.search,
                    color: grey3,
                    size: 20,
                  ),
                  suffixIcon: searchController.text.isNotEmpty
                      ? GestureDetector(
                          onTap: _clearSearch,
                          child: Icon(
                            Icons.clear,
                            color: grey3,
                            size: 20,
                          ),
                        )
                      : null,
                  border: InputBorder.none,
                  contentPadding:
                      EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                ),
                style: TextStyle(
                  fontFamily: 'Poppins',
                  fontSize: 14,
                  color: titlecolor,
                ),
              ),
            ),
          ),
          SizedBox(width: 12),
          // Cancel Button
          GestureDetector(
            onTap: () => Navigator.pop(context),
            child: Text(
              'Cancel',
              style: TextStyle(
                fontFamily: 'Poppins',
                fontSize: 16,
                fontWeight: FontWeight.w600,
                color: primaryColor,
              ),
            ),
          ),
        ],
      ),
    );
  }

  /// Build individual contact card
  Widget _buildContactCard(Map<String, dynamic> contact) {
    return Container(
      margin: EdgeInsets.symmetric(horizontal: 20, vertical: 8),
      decoration: BoxDecoration(
        color: whiteColor,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.05),
            blurRadius: 10,
            offset: Offset(0, 2),
          ),
        ],
      ),
      child: Padding(
        padding: EdgeInsets.all(16),
        child: Row(
          children: [
            // Profile Image (Red Container)
            Container(
              width: 48,
              height: 48,
              decoration: BoxDecoration(
                color: Colors.red,
                borderRadius: BorderRadius.circular(24),
              ),
              child: Center(
                child: Icon(
                  Icons.person,
                  color: whiteColor,
                  size: 24,
                ),
              ),
            ),
            SizedBox(width: 16),
            // Contact Info
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    contact['name'] ?? 'Unknown Contact',
                    style: TextStyle(
                      fontFamily: 'Poppins',
                      fontSize: 16,
                      fontWeight: FontWeight.w600,
                      color: titlecolor,
                    ),
                  ),
                  SizedBox(height: 4),
                  Text(
                    contact['role'] ?? 'No role specified',
                    style: TextStyle(
                      fontFamily: 'Poppins',
                      fontSize: 14,
                      color: grey3,
                    ),
                  ),
                  SizedBox(height: 2),
                  Text(
                    contact['institution'] ?? 'No institution specified',
                    style: TextStyle(
                      fontFamily: 'Poppins',
                      fontSize: 12,
                      color: grey3,
                    ),
                  ),
                ],
              ),
            ),
            // Add Button
            GestureDetector(
              onTap: () => _addContact(contact),
              child: Container(
                width: 40,
                height: 40,
                decoration: BoxDecoration(
                  color: primaryColor,
                  borderRadius: BorderRadius.circular(20),
                ),
                child: Center(
                  child: Icon(
                    Icons.add,
                    color: whiteColor,
                    size: 20,
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  /// Build loading widget
  Widget _buildLoadingWidget() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          CircularProgressIndicator(
            color: primaryColor,
            strokeWidth: 2,
          ),
          SizedBox(height: 16),
          Text(
            'Loading contacts...',
            style: TextStyle(
              fontFamily: 'Poppins',
              fontSize: 16,
              color: grey3,
            ),
          ),
        ],
      ),
    );
  }

  /// Build empty state widget
  Widget _buildEmptyState() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            Icons.search_off,
            size: 64,
            color: grey3,
          ),
          SizedBox(height: 16),
          Text(
            isSearching ? 'No contacts found' : 'No contacts available',
            style: TextStyle(
              fontFamily: 'Poppins',
              fontSize: 18,
              fontWeight: FontWeight.w600,
              color: titlecolor,
            ),
          ),
          SizedBox(height: 8),
          Text(
            isSearching
                ? 'Try searching with different keywords'
                : 'Contacts will appear here once loaded',
            style: TextStyle(
              fontFamily: 'Poppins',
              fontSize: 14,
              color: grey3,
            ),
          ),
        ],
      ),
    );
  }

  /// Build see more button
  Widget _buildSeeMoreButton() {
    return Container(
      padding: EdgeInsets.symmetric(vertical: 20),
      child: Center(
        child: GestureDetector(
          onTap: () {
            // TODO: Implement pagination or load more functionality
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(
                content: Text('Load more functionality coming soon!'),
                backgroundColor: primaryColor,
              ),
            );
          },
          child: Text(
            'See More',
            style: TextStyle(
              fontFamily: 'Poppins',
              fontSize: 16,
              fontWeight: FontWeight.w600,
              color: primaryColor,
            ),
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: color3,
      body: SafeArea(
        child: Column(
          children: [
            // Search Header
            _buildSearchHeader(),
            // Search Results
            Expanded(
              child: isLoading
                  ? _buildLoadingWidget()
                  : filteredContacts.isEmpty
                      ? _buildEmptyState()
                      : ListView.builder(
                          padding: EdgeInsets.symmetric(vertical: 8),
                          itemCount: filteredContacts.length +
                              1, // +1 for See More button
                          itemBuilder: (context, index) {
                            if (index == filteredContacts.length) {
                              return _buildSeeMoreButton();
                            }
                            return _buildContactCard(filteredContacts[index]);
                          },
                        ),
            ),
          ],
        ),
      ),
    );
  }
}
