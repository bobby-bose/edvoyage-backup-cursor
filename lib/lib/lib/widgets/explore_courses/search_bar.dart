import 'package:flutter/material.dart';
import 'package:notes/utils/colors/colors.dart';

class SearchBar extends StatelessWidget {
  const SearchBar({super.key});

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: 30,
      child: TextFormField(
        decoration: InputDecoration(
          fillColor: Colors.black12,
          filled: true,
          isDense: true,
          contentPadding: EdgeInsets.fromLTRB(5, 5, 5, 0),
          hintText: "Search University or Course",
          hintStyle: TextStyle(fontFamily: 'Poppins', color: textColor),
          prefixIcon: Icon(Icons.search, color: iconcolor, size: 20),
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(40.0),
            borderSide: BorderSide(color: grey2),
          ),
          enabledBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(40.0),
            borderSide: BorderSide(color: Colors.black12),
          ),
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(40.0),
            borderSide: BorderSide(color: grey2),
          ),
        ),
      ),
    );
  }
}
