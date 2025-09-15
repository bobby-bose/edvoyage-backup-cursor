import 'package:flutter/material.dart';

class CustomLogoAppBar extends StatefulWidget implements PreferredSizeWidget {
  const CustomLogoAppBar({super.key});

  @override
  State<CustomLogoAppBar> createState() => _CustomLogoAppBarState();

  @override
  Size get preferredSize => const Size.fromHeight(kToolbarHeight);
}

class _CustomLogoAppBarState extends State<CustomLogoAppBar> {
  @override
  Widget build(BuildContext context) {
    final currentWidth = MediaQuery.of(context).size.width * 0.5;

    return AppBar(
      leading: Navigator.canPop(context)
          ? IconButton(
              icon: const Icon(
                Icons.arrow_back,
                // add a color of dark green
                color: Color(0xFF008080),

                size: 30,
              ),
              onPressed: () => Navigator.of(context).pop(),
            )
          : null,
      automaticallyImplyLeading: false,
      backgroundColor: Colors.white,
      elevation: 1.0,
      title: Padding(
        padding: const EdgeInsets.only(top: 15.0),
        child: SizedBox(
          width: currentWidth, // take full width
          child: Image.asset(
            'assets/edvoyage1.png', // update path if needed
            width: currentWidth,
            fit: BoxFit.contain, // keep proportions
          ),
        ),
      ),
      centerTitle: true, // ensures it's centered in AppBar
    );
  }
}
