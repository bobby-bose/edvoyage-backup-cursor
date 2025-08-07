import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../../utils/BottomNavigation/bottom_navigation.dart';
import '../../utils/colors/colors.dart';
import '../../utils/responsive.dart';

class ProfileInfo extends StatefulWidget {
  const ProfileInfo({super.key});

  @override
  _ProfileInfoState createState() => _ProfileInfoState();
}

class _ProfileInfoState extends State<ProfileInfo> {
  final TextEditingController _nameController = TextEditingController();
  File? _image;

  Future<void> _pickImage() async {
    final picker = ImagePicker();
    final pickedImage = await picker.pickImage(source: ImageSource.gallery);

    setState(() {
      if (pickedImage != null) {
        _image = File(pickedImage.path);
      }
    });
  }

  Future<void> _saveProfile() async {
    final sharedPreferences = await SharedPreferences.getInstance();
    await sharedPreferences.setString('name', _nameController.text);
    if (_image != null) {
      await sharedPreferences.setString('image', _image!.path);
    }
    Navigator.push(context,
        PageRouteBuilder(pageBuilder: (_, __, ___) => BottomNavigation()));
  }

  @override
  void dispose() {
    _nameController.dispose();
    super.dispose();
  }

  Measurements? size;

  @override
  Widget build(BuildContext context) {
    size = Measurements(MediaQuery.of(context).size);
    return Scaffold(
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.only(top: 100, right: 50, left: 50),
          child: Column(
            children: [
              Text(
                'Profile Info',
                textScaleFactor: 2,
                style: TextStyle(
                    fontFamily: 'Roboto',
                    fontWeight: FontWeight.w700,
                    color: primaryColor),
              ),
              vGap(15),
              Text(
                'Please provide your name and an optional photo',
                style: TextStyle(
                    fontFamily: 'Roboto', fontWeight: FontWeight.w400),
              ),
              vGap(30),
              Container(
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                  ),
                  child: _image != null
                      ? CircleAvatar(
                          radius: 60,
                          backgroundImage: FileImage(File(_image!.path)),
                        )
                      : CircleAvatar(
                          backgroundColor: grey1,
                          radius: 64,
                          child: TextButton(
                              onPressed: _pickImage,
                              child: Icon(
                                Icons.camera_alt_outlined,
                                color: grey3,
                                size: 40,
                              )))),
              vGap(20),
              TextFormField(
                controller: _nameController,
                decoration: InputDecoration(
                  hintText: 'Type your name here',
                ),
              ),
              vGap(150),
              Container(
                height: size?.hp(5),
                width: size?.wp(37),
                decoration: BoxDecoration(
                    color: secondaryColor,
                    borderRadius: BorderRadius.circular(10)),
                child: TextButton(
                  onPressed: () async {
                    if (_image == null) {
                      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                          action: SnackBarAction(
                            label: 'OK',
                            onPressed: () {
                              ScaffoldMessenger.of(context)
                                  .hideCurrentSnackBar();
                            },
                          ),
                          backgroundColor: Colors.red,
                          content: Text(
                            'Please upload your photo and your name',
                            style: TextStyle(
                              color: thirdColor,
                              fontSize: 18.0,
                            ),
                          )));
                    } else {
                      _saveProfile();
                    }
                  },
                  child: Text(
                    'next',
                    style: TextStyle(color: thirdColor),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
