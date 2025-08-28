from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from .models import FavouriteUniversity, FavouriteCourse
from .serializers import FavouriteUniversitySerializer, FavouriteCourseSerializer
from universities.models import University
from courses.models import Course
from users.models import User
import traceback

class FavouriteUniversityView(APIView):
    def get(self, request):
        """Get all favourite universities for the current user"""
        try:
            print("🔍 DEBUG: Starting FavouriteUniversityView.get()")
           
           
    
            
            print("🔍 DEBUG: Attempting to filter FavouriteUniversity objects")
            try:
                favourites = FavouriteUniversity.objects.all()
                # favourites_count = favourites.count()
                # print(f"✅ DEBUG: Found {favourites_count} favourite universities")
                
                if favourites.exists():
                    first_fav = favourites.first()
                    print(f"✅ DEBUG: First favourite - User: {first_fav.user.username}, University: {first_fav.university.name}")
                else:
                    print("ℹ️ DEBUG: No favourite universities found")
                    
            except Exception as e:
                print(f"❌ DEBUG: Error filtering FavouriteUniversity: {str(e)}")
                print(f"❌ DEBUG: Traceback: {traceback.format_exc()}")
                return Response({
                    'status': 'error',
                    'message': f'Database error: {str(e)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            print("🔍 DEBUG: Attempting to serialize data")
            try:
                serializer = FavouriteUniversitySerializer(favourites, many=True)
                print(f"✅ DEBUG: Serialization successful, data count: {len(serializer.data)}")
            except Exception as e:
                print(f"❌ DEBUG: Error serializing data: {str(e)}")
                print(f"❌ DEBUG: Traceback: {traceback.format_exc()}")
                return Response({
                    'status': 'error',
                    'message': f'Serialization error: {str(e)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            print("✅ DEBUG: Returning successful response")
            return Response({
                'status': 'success',
                'data': serializer.data,
                'count': len(serializer.data)
            })
            
        except Exception as e:
            print(f"❌ DEBUG: Unexpected error in FavouriteUniversityView.get(): {str(e)}")
            print(f"❌ DEBUG: Traceback: {traceback.format_exc()}")
            return Response({
                'status': 'error',
                'message': f'Unexpected error: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        """Add a university to favourites"""
        try:
            print("🔍 DEBUG: Starting FavouriteUniversityView.post()")
            
            university_id = request.data.get('university_id')
            print(f"🔍 DEBUG: Received university_id: {university_id}")
            
            if not university_id:
                print("❌ DEBUG: No university_id provided")
                return Response({
                    'status': 'error',
                    'message': 'university_id is required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            print("🔍 DEBUG: Attempting to get university")
            try:
                university = University.objects.get(id=university_id)
                print(f"✅ DEBUG: Found university: {university.name} (ID: {university.id})")
            except University.DoesNotExist:
                print(f"❌ DEBUG: University with ID={university_id} not found")
                return Response({
                    'status': 'error',
                    'message': 'University not found'
                }, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                print(f"❌ DEBUG: Error getting university: {str(e)}")
                print(f"❌ DEBUG: Traceback: {traceback.format_exc()}")
                return Response({
                    'status': 'error',
                    'message': f'Error getting university: {str(e)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            # For testing purposes, use user ID = 1
            print("🔍 DEBUG: Attempting to get test user")
            try:
                test_user = User.objects.get(id=1)
                print(f"✅ DEBUG: Found test user: {test_user.username} (ID: {test_user.id})")
            except User.DoesNotExist:
                print("❌ DEBUG: User with ID=1 does not exist")
                return Response({
                    'status': 'error',
                    'message': 'Test user not found. Please create a user with ID=1'
                }, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                print(f"❌ DEBUG: Error getting user: {str(e)}")
                print(f"❌ DEBUG: Traceback: {traceback.format_exc()}")
                return Response({
                    'status': 'error',
                    'message': f'Error getting user: {str(e)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            # Check if already favourited
            print("🔍 DEBUG: Checking if already favourited")
            try:
                if FavouriteUniversity.objects.filter(user=test_user, university=university).exists():
                    print("❌ DEBUG: University already in favourites")
                    return Response({
                        'status': 'error',
                        'message': 'University already in favourites'
                    }, status=status.HTTP_400_BAD_REQUEST)
                print("✅ DEBUG: University not in favourites, proceeding to add")
            except Exception as e:
                print(f"❌ DEBUG: Error checking existing favourite: {str(e)}")
                print(f"❌ DEBUG: Traceback: {traceback.format_exc()}")
                return Response({
                    'status': 'error',
                    'message': f'Error checking existing favourite: {str(e)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            print("🔍 DEBUG: Creating new favourite")
            try:
                favourite = FavouriteUniversity.objects.create(user=test_user, university=university)
                print(f"✅ DEBUG: Created favourite - User: {favourite.user.username}, University: {favourite.university.name}")
            except Exception as e:
                print(f"❌ DEBUG: Error creating favourite: {str(e)}")
                print(f"❌ DEBUG: Traceback: {traceback.format_exc()}")
                return Response({
                    'status': 'error',
                    'message': f'Error creating favourite: {str(e)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            print("🔍 DEBUG: Serializing response")
            try:
                serializer = FavouriteUniversitySerializer(favourite)
                print("✅ DEBUG: Serialization successful")
            except Exception as e:
                print(f"❌ DEBUG: Error serializing response: {str(e)}")
                print(f"❌ DEBUG: Traceback: {traceback.format_exc()}")
                return Response({
                    'status': 'error',
                    'message': f'Error serializing response: {str(e)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            print("✅ DEBUG: Returning successful response")
            return Response({
                'status': 'success',
                'message': 'University added to favourites',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            print(f"❌ DEBUG: Unexpected error in FavouriteUniversityView.post(): {str(e)}")
            print(f"❌ DEBUG: Traceback: {traceback.format_exc()}")
            return Response({
                'status': 'error',
                'message': f'Unexpected error: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request):
        """Remove a university from favourites"""
        try:
            print("🔍 DEBUG: Starting FavouriteUniversityView.delete()")
            
            university_id = request.data.get('university_id')
            print(f"🔍 DEBUG: Received university_id: {university_id}")
            
            if not university_id:
                print("❌ DEBUG: No university_id provided")
                return Response({
                    'status': 'error',
                    'message': 'university_id is required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # For testing purposes, use user ID = 1
            print("🔍 DEBUG: Attempting to get test user")
            try:
                test_user = User.objects.get(id=1)
                print(f"✅ DEBUG: Found test user: {test_user.username} (ID: {test_user.id})")
            except User.DoesNotExist:
                print("❌ DEBUG: User with ID=1 does not exist")
                return Response({
                    'status': 'error',
                    'message': 'Test user not found. Please create a user with ID=1'
                }, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                print(f"❌ DEBUG: Error getting user: {str(e)}")
                print(f"❌ DEBUG: Traceback: {traceback.format_exc()}")
                return Response({
                    'status': 'error',
                    'message': f'Error getting user: {str(e)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            print("🔍 DEBUG: Attempting to delete favourite")
            try:
                favourite = FavouriteUniversity.objects.get(user=test_user, university_id=university_id)
                print(f"✅ DEBUG: Found favourite to delete - User: {favourite.user.username}, University: {favourite.university.name}")
                favourite.delete()
                print("✅ DEBUG: Favourite deleted successfully")
            except FavouriteUniversity.DoesNotExist:
                print(f"❌ DEBUG: Favourite not found for user ID=1 and university ID={university_id}")
                return Response({
                    'status': 'error',
                    'message': 'University not in favourites'
                }, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                print(f"❌ DEBUG: Error deleting favourite: {str(e)}")
                print(f"❌ DEBUG: Traceback: {traceback.format_exc()}")
                return Response({
                    'status': 'error',
                    'message': f'Error deleting favourite: {str(e)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            print("✅ DEBUG: Returning successful response")
            return Response({
                'status': 'success',
                'message': 'University removed from favourites'
            })
            
        except Exception as e:
            print(f"❌ DEBUG: Unexpected error in FavouriteUniversityView.delete(): {str(e)}")
            print(f"❌ DEBUG: Traceback: {traceback.format_exc()}")
            return Response({
                'status': 'error',
                'message': f'Unexpected error: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FavouriteCourseView(APIView):
    def get(self, request):
        """Get all favourite courses for the current user"""
        
        favourites = FavouriteCourse.objects.all()
        print("🔍 DEBUG: Favourites found:", favourites)
        serializer = FavouriteCourseSerializer(favourites, many=True)
        print("🔍 DEBUG: Serialized data:", serializer.data)
        return Response({
            'status': 'success',
            'data': serializer.data,
            'count': len(serializer.data)
        })
    
    def post(self, request):
        """Add a course to favourites"""
        course_id = request.data.get('course_id')
        if not course_id:
            return Response({
                'status': 'error',
                'message': 'course_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Course not found'
            }, status=status.HTTP_404_NOT_FOUND)

        try:
            test_user = User.objects.get(id=1)
        except User.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Test user not found. Please create a user with ID=1'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Check if already favourited
        if FavouriteCourse.objects.filter(user=test_user, course=course).exists():
            return Response({
                'status': 'error',
                'message': 'Course already in favourites'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        favourite = FavouriteCourse.objects.create(user=test_user, course=course)
        serializer = FavouriteCourseSerializer(favourite)
        print("The data for the favourite serializers are", serializer.data)
        return Response({
            'status': 'success',
            'message': 'Course added to favourites',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
    
    def delete(self, request):
        """Remove a course from favourites"""
        course_id = request.data.get('course_id')
        if not course_id:
            return Response({
                'status': 'error',
                'message': 'course_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # For testing purposes, use user ID = 1
        try:
            test_user = User.objects.get(id=1)
        except User.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Test user not found. Please create a user with ID=1'
            }, status=status.HTTP_404_NOT_FOUND)
        
        try:
            favourite = FavouriteCourse.objects.get(user=test_user, course_id=course_id)
            favourite.delete()
            return Response({
                'status': 'success',
                'message': 'Course removed from favourites'
            })
        except FavouriteCourse.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Course not in favourites'
            }, status=status.HTTP_404_NOT_FOUND)

# Legacy views for backward compatibility
class AddFavouriteUniversity(APIView):
    def post(self, request):
        
        print("🔍 DEBUG: Starting AddFavouriteUniversity.post()")
        print(f"🔍 DEBUG: Request data: {request.data}")
        print(f"🔍 DEBUG: Request method: {request.method}")
        print(f"🔍 DEBUG: Content type: {request.content_type}")    
        
        # Check for both field names for compatibility
        university_id = request.data.get('university_id') or request.data.get('university')
        print(f"🔍 DEBUG: Extracted university_id: {university_id}")
        
        if not university_id:
            print("❌ DEBUG: No university_id/university provided in request data")
            print(f"❌ DEBUG: Available keys in request.data: {list(request.data.keys())}")
            return Response({
                'status': 'error',
                'message': 'university_id or university is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        print(f"🔍 DEBUG: Attempting to get university with ID: {university_id}")
        try:
            university = University.objects.get(id=university_id)
            print(f"✅ DEBUG: Found university: {university.name} (ID: {university.id})")
        except University.DoesNotExist:
            print(f"❌ DEBUG: University with ID={university_id} not found")
            return Response({
                'status': 'error',
                'message': 'University not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"❌ DEBUG: Error getting university: {str(e)}")
            print(f"❌ DEBUG: Traceback: {traceback.format_exc()}")
            return Response({
                'status': 'error',
                'message': f'Error getting university: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # For testing purposes, use user ID = 1
        print("🔍 DEBUG: Attempting to get test user with ID=1")
        try:
            test_user = User.objects.get(id=1)
            print(f"✅ DEBUG: Found test user: {test_user.username} (ID: {test_user.id})")
        except User.DoesNotExist:
            print("❌ DEBUG: User with ID=1 does not exist")
            return Response({
                'status': 'error',
                'message': 'Test user not found. Please create a user with ID=1'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"❌ DEBUG: Error getting user: {str(e)}")
            print(f"❌ DEBUG: Traceback: {traceback.format_exc()}")
            return Response({
                'status': 'error',
                'message': f'Error getting user: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        print("🔍 DEBUG: Checking if university is already in favourites")
        existing_favourite = FavouriteUniversity.objects.filter(user=test_user, university=university).first()
        
        if existing_favourite:
            # University already exists in favourites, so delete it (toggle off)
            print(f"🔍 DEBUG: University {university.name} is already in favourites for user {test_user.username}, removing it...")
            try:
                existing_favourite.delete()
                print(f"✅ DEBUG: Successfully removed favourite: User={test_user.username}, University={university.name}")
                return Response({
                    'status': 'success',
                    'message': 'University removed from favourites',
                    'action': 'removed'
                }, status=status.HTTP_200_OK)
            except Exception as e:
                print(f"❌ DEBUG: Error removing favourite: {str(e)}")
                print(f"❌ DEBUG: Traceback: {traceback.format_exc()}")
                return Response({
                    'status': 'error',
                    'message': f'Error removing favourite: {str(e)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            # University doesn't exist in favourites, so create it (toggle on)
            print("🔍 DEBUG: Creating new favourite university entry")
            try:
                favourite = FavouriteUniversity.objects.create(user=test_user, university=university)
                print(f"✅ DEBUG: Successfully created favourite: User={test_user.username}, University={university.name}")
                return Response({
                    'status': 'success',
                    'message': 'University added to favourites',
                    'action': 'added'
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                print(f"❌ DEBUG: Error creating favourite: {str(e)}")
                print(f"❌ DEBUG: Traceback: {traceback.format_exc()}")
                return Response({
                    'status': 'error',
                    'message': f'Error creating favourite: {str(e)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AddFavouriteCourse(APIView):
    def post(self, request):
        print("🔍 DEBUG: Starting AddFavouriteCourse.post()")
        print(f"🔍 DEBUG: Request data: {request.data}")
        print(f"🔍 DEBUG: Request method: {request.method}")
        print(f"🔍 DEBUG: Content type: {request.content_type}")
        
        course_id = request.data.get('course')
        print(f"🔍 DEBUG: Extracted course_id: {course_id}")
        
        if not course_id:
            print("❌ DEBUG: No course_id provided in request data")
            print(f"❌ DEBUG: Available keys in request.data: {list(request.data.keys())}")
            return Response({
                'status': 'error',
                'message': 'course is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Course not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # For testing purposes, use user ID = 1
        try:
            test_user = User.objects.get(id=1)
        except User.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Test user not found. Please create a user with ID=1'
            }, status=status.HTTP_404_NOT_FOUND)
        
        existing_favourite = FavouriteCourse.objects.filter(user=test_user, course=course).first()
        
        if existing_favourite:
            # Course already exists in favourites, so delete it (toggle off)
            print(f"🔍 DEBUG: Course {course.name} is already in favourites for user {test_user.username}, removing it...")
            try:
                existing_favourite.delete()
                print(f"✅ DEBUG: Successfully removed favourite course: User={test_user.username}, Course={course.name}")
                return Response({
                    'status': 'success',
                    'message': 'Course removed from favourites',
                    'action': 'removed'
                }, status=status.HTTP_200_OK)
            except Exception as e:
                print(f"❌ DEBUG: Error removing favourite course: {str(e)}")
                print(f"❌ DEBUG: Traceback: {traceback.format_exc()}")
                return Response({
                    'status': 'error',
                    'message': f'Error removing favourite course: {str(e)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            # Course doesn't exist in favourites, so create it (toggle on)
            print("🔍 DEBUG: Creating new favourite course entry")
            try:
                favourite = FavouriteCourse.objects.create(user=test_user, course=course)
                print(f"✅ DEBUG: Successfully created favourite course: User={test_user.username}, Course={course.name}")
                return Response({
                    'status': 'success',
                    'message': 'Course added to favourites',
                    'action': 'added'
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                print(f"❌ DEBUG: Error creating favourite course: {str(e)}")
                print(f"❌ DEBUG: Traceback: {traceback.format_exc()}")
                return Response({
                    'status': 'error',
                    'message': f'Error creating favourite course: {str(e)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
