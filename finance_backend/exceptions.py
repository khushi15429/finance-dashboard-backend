from rest_framework.views     import exception_handler
from rest_framework.response  import Response
from rest_framework           import status


def custom_exception_handler(exc, context):
    """
    Wraps all DRF errors in a consistent response format:
    {
        "success": false,
        "error":   "Error type",
        "detail":  "Human readable message",
        "errors":  { field: [messages] }   <-- only for validation errors
    }
    """
    response = exception_handler(exc, context)

    if response is not None:
        error_data = {
            'success': False,
            'status':  response.status_code,
        }

        # validation errors (400) — have field-level detail
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            error_data['error']  = 'Validation error'
            error_data['errors'] = response.data

        # authentication errors (401)
        elif response.status_code == status.HTTP_401_UNAUTHORIZED:
            error_data['error']  = 'Authentication required'
            error_data['detail'] = 'Please provide a valid token.'

        # permission errors (403)
        elif response.status_code == status.HTTP_403_FORBIDDEN:
            error_data['error']  = 'Permission denied'
            error_data['detail'] = str(
                response.data.get('detail', 'You do not have permission.')
            )

        # not found errors (404)
        elif response.status_code == status.HTTP_404_NOT_FOUND:
            error_data['error']  = 'Not found'
            error_data['detail'] = 'The requested resource does not exist.'

        # method not allowed (405)
        elif response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED:
            error_data['error']  = 'Method not allowed'
            error_data['detail'] = str(response.data.get('detail', ''))

        # everything else
        else:
            error_data['error']  = 'Server error'
            error_data['detail'] = str(response.data)

        response.data = error_data

    return response