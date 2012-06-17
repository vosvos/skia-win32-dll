#include <windows.h>    /* This enables access to Microsoft Windows specific data types that are required to use the Graphical User Interface of Windows. (HWND, WNDCLASSEX, etc.)    */
#include <tchar.h> /* _T */


#include "ext/canvas_paint_win.h"
#include "include/effects/SkBlurDrawLooper.h"
#include "SkRandom.h"
#include "SkTypeface.h"

LRESULT CALLBACK WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam); /* A 'Forward Declaration' of a function that will mainly handle user interaction with our window.    */

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) /* The 'entry' point of the program. Console programs use the simple main(...)        */
{
    MSG msg                = {0};                            /* Required to detect user clicking on the X of the window which equals to sending a 'WM_CLOSE' 'message'                    */
    WNDCLASSEX wcex        = {0};                            /* Required information that the Microsoft Windows Operating System needs of a new window are stored in this struct.        */
    wcex.cbSize            = sizeof(WNDCLASSEX);            /* Set the size of the incoming 'preparation information'                                                                    */
    wcex.lpfnWndProc    = WndProc;                        /* Set which function will receive this windows messages, for example: clicking on this windows X                            */
    wcex.hInstance      = hInstance;                    /* Windows uses this to keep track of multiple instances of this program with the same window class name.                    */
    //wcex.hbrBackground  = (HBRUSH)(COLOR_BACKGROUND);    /* This is the background color to use for this window. It conforms to custom window background colors defined by the user    */
    wcex.hbrBackground  = (HBRUSH)(COLOR_WINDOW+1);
    wcex.lpszClassName  = L"minwindowsapp";                /* This is the base name of this type of a window, and can be reused to create the same 'style' windows easier again.        */
    if( FAILED(RegisterClassEx(&wcex)) )                /* This asks the operating system if it has resources to allow us to register a new 'style' of a window to be used.            */
        return 1;                                        /* If there were no resources available, the program will terminate by returning the number 1. (0 usually means success)    */

    if(FAILED(CreateWindow(wcex.lpszClassName,            /* the '...if(FAILED(...' part will perform the 'return 2;' command if there was an error during the creation of the window.*/
                        L"Minimal Windows Application", /* This is the actual name shown in the 'title bar' of the window. The L before the quotes, simplified, means its UNICODE.    */
                        WS_OVERLAPPEDWINDOW|WS_VISIBLE, /* WS_OVERLAPPEDWINDOW gives the window a title bar, a window menu, a sizing border, and minimize and maximize buttons.        */
                        0,                                /* Initial X position of the window.                                                                                        */
                        0,                                /* Initial Y position of the window.                                                                                        */
                        640,                            /* Initial Width of the window.                                                                                                */
                        480,                            /* Initial Height of the window.                                                                                            */
                        0,                                /* Here could be a 'handle' to the parent or owner window of this window.                                                    */
                        0,                                /* Here could be a 'handle' to a menu (usually constructed with the GUI tools of Visual Studio).                            */
                        hInstance,                        /* The 'handle' or 'unique id' of the instance of this program that will be associated with the to-be-created window(class).*/
                        NULL)))                            /* This last parameter is used in advanced windows programming like abstracting the functionality of WndProc etc.            */
        return 2;                                        /* Number 2 is returned to keep track in which part of this programs execution did the program fail. This style is optional.*/

    while( GetMessage( &msg, NULL, 0, 0 ) )                /* This checks user 'messages', and if our window is for example clicked, the 'message' will go to our WndProc function.    */
    {
        DispatchMessage( &msg );                        /* Sends the messages that were relevant to our window to the WndProc function we have defined for our window class.        */
    }

    return 0;                                            /* Everything went ok, return 0 as a sign of successful program termination.                                                */
}


void DoPaint (HWND hwnd)
{
    skia::PlatformCanvasPaint canvas (hwnd); // opaque false - 
    /*http://www.chromium.org/developers/design-documents/graphics-and-skia
    The case of the disappearing alpha
    Windows causes some problems by not knowing about the alpha channel. When rendering text, it 
    inconveniently sets the alpha channel to 0 (transparent). This makes black text fully transparent, 
    and white text becomes "interesting" because the color values are not value premultiplied colors. 
    We have two approaches to dealing with this, one for the Webkit port, and the other for the UI. 
    We may merge or enhance these in the future.
    */

    if (canvas.isEmpty ())
        return;

    canvas.save();
    canvas.drawARGB (255, 255, 255, 255); // Fill with white.
    
    canvas.rotate(SkIntToScalar (46));

    // Make a rect from (100,0) to (200,75).
    SkRect rect;
    rect.set(SkIntToScalar(100), SkIntToScalar(10),
             SkIntToScalar(200), SkIntToScalar(75));

    // Create a path with that rect and rounded corners of radius 10.
    SkPath path;
    path.addRoundRect(rect, SkIntToScalar(10), SkIntToScalar(10));

    // Fill the path (with antialiasing) in 50% transparent green.
    SkPaint paint;
    paint.setStyle(SkPaint::kFill_Style);
    paint.setFlags(SkPaint::kAntiAlias_Flag);
    paint.setARGB(128, 0, 255, 0);

    // Make a shadow!
    double blur = 1.87;
    double width = 3;
    double height = 2;

    SkColor c = SkColorSetARGB(0xFF/7, 0, 0, 0);
    SkBlurDrawLooper dl (SkDoubleToScalar(blur/2), SkDoubleToScalar(width), SkDoubleToScalar(height), c);
    paint.setLooper (&dl);

    canvas.drawPath(path, paint);
    canvas.restore ();
    paint.setARGB(64, 0, 0, 255);
    canvas.drawPath(path, paint);
    paint.setLooper (0);


    paint.setARGB(64, 255, 0, 0);
    canvas.drawCircle (SkIntToScalar(55), SkIntToScalar(55), SkIntToScalar(15), paint);

    canvas.save();
    canvas.rotate(SkIntToScalar (-15));

    //Turn AntiAliasing On
    paint.setAntiAlias(true);
    paint.setLCDRenderText(true);
    paint.setSubpixelText(true);
    paint.setTypeface(SkTypeface::CreateFromName("arial", SkTypeface::kNormal));

    //Set Text Size
    paint.setTextSize(SkIntToScalar(64));
    //paint.setLooper (&dl); // causes runtime error in Debug version (Release works)
    canvas.drawText("Rotated Text", 12, SkIntToScalar(0), SkIntToScalar(400), paint);
    canvas.restore();


    SkPath curves;
    curves.moveTo(30, 30);
    curves.cubicTo(30, 5, 50, 5, 50, 30);
    curves.cubicTo(50, 80, 150, 5, 150, 70);

    SkPaint paint2;
    paint2.setAntiAlias(true);
    paint2.setStyle(SkPaint::kStroke_Style);
    paint2.setStrokeWidth(1);
    paint2.setColor(SK_ColorRED);

    canvas.save();
    canvas.translate(100,100);
    canvas.scale(2 * SK_Scalar1, 2 * SK_Scalar1);
    canvas.drawPath(curves, paint2);
    canvas.restore();

}


LRESULT CALLBACK WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam) /* The implementation of our forward declaration. A common 'message loop' or, 'Window Procedure'    */
{
	//PAINTSTRUCT ps;
    //HDC hdc;
    TCHAR greeting[] = _T("Hello, World!");

	switch(message)                                        /* The message that our window has received can be caught using various 'defines' like: WM_LBUTTONUP, WM_KEYDOWN, etc. :)    */
    {
	case WM_PAINT:
		DoPaint (hWnd);
        return 0;
		//hdc = BeginPaint(hWnd, &ps);

        // Here your application is laid out.
        // For this introduction, we just print out "Hello, World!"
        // in the top left corner.
        //TextOut(hdc, 5, 5, greeting, _tcslen(greeting));
        // End application-specific layout section.

        //EndPaint(hWnd, &ps);
        break;
    case WM_CLOSE:                                        /* The user clicked the 'X' at the top right of the window, we caught the message with GetMessage() and processed it here :)*/
        PostQuitMessage(0);                                /* This requests Windows the permission to terminate (quit). GetMessage catches that, returns false, and ends the while loop*/
        break;
    default:                                            /* If no 'case' condition matched the content of the message received, return DefWindowProc(...)                            */
        return DefWindowProc(hWnd, message, wParam, lParam); /* Our application specified no action for the received message(say for WM_KEYDOWN),pass the message along to 'others'.*/
    }
    return 0;                                            /* Zero return value from a window procedure usually means the message was not 'caught' or 'used' within the message switch.*/
}



