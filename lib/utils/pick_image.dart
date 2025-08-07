import 'dart:io';

import 'package:image_picker/image_picker.dart';
import 'package:firebase_storage/firebase_storage.dart';

Future<List<int>?> pickImage(ImageSource source) async {
  ImagePicker imagePicker = ImagePicker();
  XFile? image = await imagePicker.pickImage(source: source);

  if (image != null) {
    FirebaseStorage storage = FirebaseStorage.instance;
    Reference ref = storage.ref().child('images/${DateTime.now().toString()}');
    await ref.putFile(File(image.path));
    String imageUrl = await ref.getDownloadURL();

    // Note: The following code reads the image as bytes, you might want to adjust this based on your needs.
    File file = File(image.path);
    List<int> bytes = await file.readAsBytes();
    return bytes;
  }

  return null;
}
