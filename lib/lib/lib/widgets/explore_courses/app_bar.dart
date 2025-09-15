import 'package:flutter/material.dart';

import 'package:notes/utils/colors/colors.dart';

class CustomAppBar extends StatelessWidget {
  const CustomAppBar({super.key});

  @override
  Widget build(BuildContext context) {
    return AppBar(
      shape: ContinuousRectangleBorder(
        borderRadius: BorderRadius.only(
          bottomLeft: Radius.circular(150.0),
          bottomRight: Radius.circular(150.0),
        ),
      ),
      toolbarHeight: 70.0,
      primary: false,
      backgroundColor: Colors.white,
      title: SearchBar(),
      leading: buildBackButton(context),
      actions: [buildFilterButton(context)],
    );
  }

  Widget buildBackButton(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(left: 20.0),
      child: IconButton(
        onPressed: () {
          Navigator.pop(context);
        },
        icon: Icon(Icons.arrow_back_ios, color: Cprimary),
      ),
    );
  }

  Widget buildFilterButton(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.only(right: 15.0),
        child: IconButton(
          onPressed: () {
            // Navigator.push(
            //     context, MaterialPageRoute(builder: (context) => SortHome()));
          },
          icon: Image.asset("assets/filter.png"),
        ),
      ),
    );
  }
}
