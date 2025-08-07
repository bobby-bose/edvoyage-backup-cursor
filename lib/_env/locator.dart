import 'package:get_it/get_it.dart';

import 'package:frontend/Services/api_client.dart';

final getIt = GetIt.instance;

void setup() {
  getIt.registerSingleton<ApiClient>(ApiClient());
}
