import 'package:flutter/material.dart';

import '../utils/colors/colors.dart';

class BackArrow extends StatelessWidget {
  const BackArrow({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      child: IconButton(
        onPressed: () {
          Navigator.pop(context);
        },
        icon: Icon(Icons.arrow_back_rounded, size: 30, color: primaryColor),
      ),
    );
  }
}
