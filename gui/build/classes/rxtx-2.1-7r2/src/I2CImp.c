/*-------------------------------------------------------------------------
|   rxtx is a native interface to i2c ports in java.
|   Copyright 1997-2004 by Trent Jarvi taj@www.linux.org.uk
|
|   This library is free software; you can redistribute it and/or
|   modify it under the terms of the GNU Library General Public
|   License as published by the Free Software Foundation; either
|   version 2 of the License, or (at your option) any later version.
|
|   This library is distributed in the hope that it will be useful,
|   but WITHOUT ANY WARRANTY; without even the implied warranty of
|   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
|   Library General Public License for more details.
|
|   You should have received a copy of the GNU Library General Public
|   License along with this library; if not, write to the Free
|   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
--------------------------------------------------------------------------*/
#if defined(__MWERKS__) /* dima */
#include "I2C.h" /* dima */
#else /* dima */
#include "config.h"
#include "gnu_io_I2C.h"
#endif /* dima */
#include <time.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <errno.h>
#ifndef WIN32
#include <sys/ioctl.h>
#include <sys/param.h>
#include <sys/utsname.h>
#ifdef HAVE_TERMIOS_H
#	include <termios.h>
#endif
#ifdef HAVE_SYS_SIGNAL_H
#   include <sys/signal.h>
#endif
#else
#	include <win32termios.h>
#endif
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/time.h>
#ifdef HAVE_SYS_FCNTL_H
#   include <sys/fcntl.h>
#endif
#ifdef HAVE_SYS_FILE_H
#   include <sys/file.h>
#endif

#if defined(__linux__)
#	include <linux/types.h> /* fix for linux-2.3.4? kernels */
#	include <linux/serial.h>
#	include <linux/version.h>
#endif

extern int errno;
#include "I2CImp.h"
/* #define DEBUG_TIMEOUT */

/*----------------------------------------------------------
I2CPort.Initialize

   accept:      none
   perform:     Initialize the native library
   return:      none
----------------------------------------------------------*/
JNIEXPORT void JNICALL Java_gnu_io_I2CPort_Initialize( 
	JNIEnv *env,
	jclass jclazz 
	)
{
#ifndef WIN32
	struct utsname name;
	/* This bit of code checks to see if there is a signal handler installed
	   for SIGIO, and installs SIG_IGN if there is not.  This is necessary
	   for the native threads jdk, but we don't want to do it with green
	   threads, because it slows things down.  Go figure. */

	/* POSIX signal handling functions */
#if !defined(__FreeBSD___)
	struct sigaction handler;
	sigaction( SIGIO, NULL, &handler );
	if( !handler.sa_handler ) signal( SIGIO, SIG_IGN );
#endif /* !__FreeBSD__ */
#if defined(__linux__) 
	/* Lets let people who upgraded kernels know they may have problems */
	if (uname (&name) == -1)
	{
		fprintf(stderr,"RXTX WARNING:  cannot get system name\n");
		return;
	}
	if(strcmp(name.release,UTS_RELEASE)!=0)
	{
		fprintf(stderr, "\n\n\nRXTX WARNING:  This library was compiled to run with OS release %s and you are currently running OS release %s.  In some cases this can be a problem.  Try recompiling RXTX if you notice strange behavior.  If you just compiled RXTX make sure /usr/include/linux is a symbolic link to the include files that came with the kernel source and not an older copy.\n\n\npress enter to continue\n",UTS_RELEASE,name.release);
		getchar();
	}
#endif /* __linux__ */
#endif /* WIN32 */
}


/*----------------------------------------------------------
I2CPort.open

   accept:      The device to open.  ie "/dev/ttyS0"
   perform:     open the device, set the termios struct to sane settings and 
                return the filedescriptor
   return:      fd
   exceptions:  IOExcepiton
   comments:    Very often people complain about not being able to get past
                this function and it turns out to be permissions on the 
                device file or bios has the device disabled.
----------------------------------------------------------*/ 
JNIEXPORT jint JNICALL Java_gnu_io_I2CPort_open( 
	JNIEnv *env, 
	jobject jobj,
	jstring jstr 
	)
{
	struct termios ttyset;
	int fd;
	const char *filename = (*env)->GetStringUTFChars( env, jstr, 0 );

	do {
		fd=open (filename, O_RDWR | O_NOCTTY | O_NONBLOCK );
	}  while (fd < 0 && errno==EINTR);
	(*env)->ReleaseStringUTFChars( env, jstr, NULL );
	if( fd < 0 ) goto fail;

	if( tcgetattr( fd, &ttyset ) < 0 ) goto fail;
	ttyset.c_iflag = INPCK;
	ttyset.c_lflag = 0;
	ttyset.c_oflag = 0;
	ttyset.c_cflag = CREAD | CS8 | CLOCAL;
	ttyset.c_cc[ VMIN ] = 0;
	ttyset.c_cc[ VTIME ] = 0;

#ifdef __FreeBSD__
	if( cfsetspeed( &ttyset, B9600 ) < 0 ) goto fail;
#else
	if( cfsetispeed( &ttyset, B9600 ) < 0 ) goto fail;
	if( cfsetospeed( &ttyset, B9600 ) < 0 ) goto fail;
#endif
	if( tcsetattr( fd, TCSANOW, &ttyset ) < 0 ) goto fail;

#ifndef WIN32
	fcntl( fd, F_SETOWN, getpid() );
	fcntl( fd, F_SETFL, FASYNC );
#endif /* WIN32 */

	return (jint)fd;

fail:
	throw_java_exception( env, IO_EXCEPTION, "open", strerror( errno ) );
	return -1;
}

/*----------------------------------------------------------
I2CPort.nativeClose

   accept:      none
   perform:     get the fd from the java end and close it
   return:      none
   exceptions:  none
----------------------------------------------------------*/ 
JNIEXPORT void JNICALL Java_gnu_io_I2CPort_nativeClose( JNIEnv *env,
	jobject jobj )
{
	int result;
	int fd = get_java_var( env, jobj,"fd","I" );

	do {
		result=close (fd);
	}  while (result < 0 && errno==EINTR);
	return;
}

/*----------------------------------------------------------
 I2CPort.nativeSetI2CPortParams

   accept:     speed, data bits, stop bits, parity
   perform:    set the i2c port parameters
   return:     void
   exceptions: UnsupportedCommOperationException
----------------------------------------------------------*/ 
JNIEXPORT void JNICALL Java_gnu_io_I2CPort_nativeSetI2CPortParams(
	JNIEnv *env, jobject jobj, jint speed, jint dataBits, jint stopBits,
	jint parity )
{
	struct termios ttyset;
	int fd = get_java_var( env, jobj,"fd","I" );
	int cspeed = translate_speed( env, speed );
	if( !cspeed ) return;
	if( tcgetattr( fd, &ttyset ) < 0 ) goto fail;
	if( !translate_data_bits( env, (int *)&(ttyset.c_cflag), dataBits ) ) return; /* dima darwin defime c_cflag as unsigned long */
	if( !translate_stop_bits( env, (int *)&(ttyset.c_cflag), stopBits ) ) return; /* dima darwin defime c_cflag as unsigned long */
	if( !translate_parity( env, (int *)&(ttyset.c_cflag), parity ) ) return;/* dima darwin defime c_cflag as unsigned long */
#ifdef __FreeBSD__
	if( cfsetspeed( &ttyset, cspeed ) < 0 ) goto fail;
#else
	if( cfsetispeed( &ttyset, cspeed ) < 0 ) goto fail;
	if( cfsetospeed( &ttyset, cspeed ) < 0 ) goto fail;
#endif
	if( tcsetattr( fd, TCSANOW, &ttyset ) < 0 ) goto fail;
	/* dump_termios("set",*ttyset); */
	return;

fail:
	throw_java_exception( env, UNSUPPORTED_COMM_OPERATION,
		"nativeSetI2CPortParams", strerror( errno ) );
}

/*----------------------------------------------------------
 translate_speed

   accept:     speed in bits-per-second
   perform:    convert bits-per-second to a speed_t constant
   return:     speed_t constant
   exceptions: UnsupportedCommOperationException
   comments:   Only the lowest level code should know about
               the magic constants.
----------------------------------------------------------*/ 
int translate_speed( JNIEnv *env, jint speed )
{
	switch( speed ) {
		case 0:		return B0;
		case 50:		return B50;
		case 75:		return B75;
		case 110:	return B110;
		case 134:	return B134;
		case 150:	return B150;
		case 200:	return B200;
		case 300:	return B300;
		case 600:	return B600;
		case 1200:	return B1200;
		case 1800:	return B1800;
		case 2400:	return B2400;
		case 4800:	return B4800;
		case 9600:	return B9600;
		case 19200:	return B19200;
		case 38400:	return B38400;
		case 57600:	return B57600;
		case 115200:	return B115200;
		case 230400:	return B230400;
#ifdef B460800
		case 460800:	return B460800;
#endif
	}

	throw_java_exception( env, UNSUPPORTED_COMM_OPERATION,
		"translate_speed", "speed" );
	return 0;
}

/*----------------------------------------------------------
 translate_data_bits

   accept:     gnu.io.I2CPort.DATABITS_* constant
   perform:    set proper termios c_cflag bits
   return:     1 if successful
					0 if an exception is thrown
   exceptions: UnsupportedCommOperationException
----------------------------------------------------------*/ 
int translate_data_bits( JNIEnv *env, int *cflag, jint dataBits )
{
	int temp = (*cflag) & ~CSIZE;

	switch( dataBits ) {
		case DATABITS_5:
			(*cflag) = temp | CS5;
			return 1;
		case DATABITS_6:
			(*cflag) = temp | CS6;
			return 1;
		case DATABITS_7:
			(*cflag) = temp | CS7;
			return 1;
		case DATABITS_8:
			(*cflag) = temp | CS8;
			return 1;
	}

	throw_java_exception( env, UNSUPPORTED_COMM_OPERATION,
		"translate_data_bits", "data bits" );
	return 0;
}

/*----------------------------------------------------------
 translate_stop_bits

   accept:     gnu.io.I2CPort.STOPBITS_* constant
   perform:    set proper termios c_cflag bits
   return:     1 if successful
					0 if an exception is thrown
   exceptions: UnsupportedCommOperationException
   comments:   If you specify 5 data bits and 2 stop bits, the port will
               allegedly use 1.5 stop bits.  Does anyone care?
----------------------------------------------------------*/ 
int translate_stop_bits( JNIEnv *env, int *cflag, jint stopBits )
{
	switch( stopBits ) {
		case STOPBITS_1:
			(*cflag) &= ~CSTOPB;
			return 1;
		case STOPBITS_2:
			(*cflag) |= CSTOPB;
			return 1;
	}

	throw_java_exception( env, UNSUPPORTED_COMM_OPERATION,
		"translate_stop_bits", "stop bits" );
	return 0;
}

/*----------------------------------------------------------
 translate_parity

   accept:     gnu.io.I2CPort.PARITY_* constant
   perform:    set proper termios c_cflag bits
   return:     1 if successful
               0 if an exception is thrown
   exceptions: UnsupportedCommOperationException
   comments:   The CMSPAR bit should be used for 'mark' and 'space' parity,
               but it's not in glibc's includes.  Oh well, rarely used anyway.
----------------------------------------------------------*/ 
int translate_parity( JNIEnv *env, int *cflag, jint parity )
{
	(*cflag) &= ~(PARENB | PARODD);
	switch( parity ) {
		case PARITY_NONE:
			return 1;
#ifdef CMSPAR
		case PARITY_EVEN:
			(*cflag) |= PARENB;
			return 1;
		case PARITY_ODD:
			(*cflag) |= PARENB | PARODD;
			return 1;
		case PARITY_MARK:
			(*cflag) |= PARENB | PARODD | CMSPAR;
			return 1;
		case PARITY_SPACE:
			(*cflag) |= PARENB | CMSPAR;
			return 1;
#else
		case PARITY_EVEN:
			(*cflag) |= PARENB;
			return 1;
		case PARITY_ODD:
			(*cflag) |= PARENB | PARODD;
			return 1;
#endif
	}

	throw_java_exception( env, UNSUPPORTED_COMM_OPERATION,
		"translate_parity", "parity" );
	return 0;
}


/*----------------------------------------------------------
I2CPort.writeByte

   accept:      byte to write (passed as int)
   perform:     write a single byte to the port
   return:      none
   exceptions:  IOException
----------------------------------------------------------*/ 
JNIEXPORT void JNICALL Java_gnu_io_I2CPort_writeByte( JNIEnv *env,
	jobject jobj, jint ji ) 
{
	unsigned char byte = (unsigned char)ji;
	int fd = get_java_var( env, jobj,"fd","I" );
	int result;

	do {
		result=write (fd, &byte, sizeof(unsigned char));
	}  while (result < 0 && errno==EINTR);
	if(result >= 0)
		return;
	throw_java_exception( env, IO_EXCEPTION, "writeByte",
		strerror( errno ) );
}


/*----------------------------------------------------------
I2CPort.writeArray

   accept:      jbarray: bytes used for writing 
                offset: offset in array to start writing
                count: Number of bytes to write
   perform:     write length bytes of jbarray
   return:      none
   exceptions:  IOException
----------------------------------------------------------*/ 
JNIEXPORT void JNICALL Java_gnu_io_I2CPort_writeArray( JNIEnv *env,
	jobject jobj, jbyteArray jbarray, jint offset, jint count )
{
	int fd = get_java_var( env, jobj,"fd","I" );
	int result=0,total=0,i;

	unsigned char *bytes = (unsigned char *)malloc( count );

	jbyte *body = (*env)->GetByteArrayElements( env, jbarray, 0 );
	for( i = 0; i < count; i++ ) bytes[ i ] = body[ i + offset ];
	(*env)->ReleaseByteArrayElements( env, jbarray, body, 0 );
	do {
		result=write (fd, bytes + total + offset, count - total); /* dima */
		if(result >0){
			total += result;
		}
	}  while ((total<count)||(result < 0 && errno==EINTR));
	free( bytes );
	if( result < 0 ) throw_java_exception( env, IO_EXCEPTION,
		"writeArray", strerror( errno ) );
}


/*----------------------------------------------------------
I2CPort.drain

   accept:      none
   perform:     wait until all data is transmitted
   return:      none
   exceptions:  IOException
   comments:    java.io.OutputStream.flush() is equivalent to tcdrain,
                not tcflush, which throws away unsent bytes

                count logic added to avoid infinite loops when EINTR is
                true...  Thread.yeild() was suggested.
----------------------------------------------------------*/
JNIEXPORT void JNICALL Java_gnu_io_I2CPort_drain( JNIEnv *env,
	jobject jobj )
{
	int fd = get_java_var( env, jobj,"fd","I" );
	int result, count=0; 

	do {
		result=tcdrain (fd);
		count++;
	}  while (result && errno==EINTR && count <5);

	if( result ) throw_java_exception( env, IO_EXCEPTION, "drain",
		strerror( errno ) );
}

/*----------------------------------------------------------
I2CPort.sendBreak

   accept:     duration in milliseconds.
   perform:    send break for actual time.  not less than 0.25 seconds.
   exceptions: none
   comments:   not very precise
----------------------------------------------------------*/ 
JNIEXPORT void JNICALL Java_gnu_io_I2CPort_sendBreak( JNIEnv *env,
	jobject jobj, jint duration )
{
	int fd = get_java_var( env, jobj,"fd","I" );
	tcsendbreak( fd, (int)( duration / 250 ) );
}


/*----------------------------------------------------------
I2CPort.NativegetReceiveTimeout

   accept:     none 
   perform:    get termios.c_cc[VTIME] 
   return:     VTIME 
   comments:   see  NativeEnableReceiveTimeoutThreshold
----------------------------------------------------------*/ 
JNIEXPORT jint JNICALL Java_gnu_io_I2CPort_NativegetReceiveTimeout(
	JNIEnv *env, 
	jobject jobj
	)
{
	int fd = get_java_var( env, jobj,"fd","I" );
	struct termios ttyset;

	if( tcgetattr( fd, &ttyset ) < 0 ) goto fail;
	return(ttyset.c_cc[ VTIME ] * 100);
fail:
	throw_java_exception( env, IO_EXCEPTION, "getReceiveTimeout", strerror( errno ) );
	return -1;
}

/*----------------------------------------------------------
I2CPort.NativeisReceiveTimeoutEnabled

   accept:     none 
   perform:    determine if VTIME is none 0 
   return:     JNI_TRUE if VTIME > 0 else JNI_FALSE 
   comments:   see  NativeEnableReceiveTimeoutThreshold
----------------------------------------------------------*/ 
JNIEXPORT jboolean JNICALL Java_gnu_io_I2CPort_NativeisReceiveTimeoutEnabled(
	JNIEnv *env, 
	jobject jobj
	)
{
	int fd = get_java_var( env, jobj,"fd","I" );
	struct termios ttyset;

	if( tcgetattr( fd, &ttyset ) < 0 ) goto fail;
	return(ttyset.c_cc[ VTIME ] > 0 ? JNI_TRUE:JNI_FALSE);
fail:
	throw_java_exception( env, IO_EXCEPTION, "isReceiveTimeoutEnabled", strerror( errno ) );
	return JNI_FALSE;
}

/*----------------------------------------------------------
I2CPort.isDSR

   accept:      none
   perform:     check status of DSR
   return:      true if TIOCM_DSR is set
                false if TIOCM_DSR is not set
   exceptions:  none
   comments:    DSR stands for Data Set Ready
----------------------------------------------------------*/
JNIEXPORT jboolean JNICALL Java_gnu_io_I2CPort_isDSR( JNIEnv *env,
	jobject jobj ) 
{
	unsigned int result = 0;
	int fd = get_java_var( env, jobj,"fd","I" );

	ioctl( fd, TIOCMGET, &result );
	if( result & TIOCM_DSR ) return JNI_TRUE;
	else return JNI_FALSE;
}

/*----------------------------------------------------------
I2CPort.isCD

   accept:      none
   perform:     check status of CD
   return:      true if TIOCM_CD is set
                false if TIOCM_CD is not set
   exceptions:  none
   comments:    CD stands for Carrier Detect
                The following comment has been made...
                "well, it works, there might ofcourse be a bug, but making DCD 
                permanently on fixed it for me so I don't care"

----------------------------------------------------------*/
JNIEXPORT jboolean JNICALL Java_gnu_io_I2CPort_isCD( JNIEnv *env,
	jobject jobj )
{
	unsigned int result = 0;
	int fd = get_java_var( env, jobj,"fd","I" );

	ioctl( fd, TIOCMGET, &result );
	if( result & TIOCM_CD ) return JNI_TRUE;
	else return JNI_FALSE;
}

/*----------------------------------------------------------
I2CPort.isCTS

   accept:      none
   perform:     check status of CTS
   return:      true if TIOCM_CTS is set
                false if TIOCM_CTS is not set
   exceptions:  none
   comments:    CTS stands for Clear To Send.
----------------------------------------------------------*/
JNIEXPORT jboolean JNICALL Java_gnu_io_I2CPort_isCTS( JNIEnv *env,
	jobject jobj ) 
{
	unsigned int result = 0;
	int fd = get_java_var( env, jobj,"fd","I" );

	ioctl( fd, TIOCMGET, &result );
	if( result & TIOCM_CTS ) return JNI_TRUE;
	else return JNI_FALSE;
}

/*----------------------------------------------------------
I2CPort.isRI

   accept:      none
   perform:     check status of RI
   return:      true if TIOCM_RI is set
                false if TIOCM_RI is not set
   exceptions:  none
   comments:    RI stands for Ring Indicator
----------------------------------------------------------*/
JNIEXPORT jboolean JNICALL Java_gnu_io_I2CPort_isRI( JNIEnv *env,
	jobject jobj )
{
	unsigned int result = 0;
	int fd = get_java_var( env, jobj,"fd","I" );

	ioctl( fd, TIOCMGET, &result );
	if( result & TIOCM_RI ) return JNI_TRUE;
	else return JNI_FALSE;
}

/*----------------------------------------------------------
I2CPort.isRTS

   accept:      none
   perform:     check status of RTS
   return:      true if TIOCM_RTS is set
                false if TIOCM_RTS is not set
   exceptions:  none
   comments:    tcgetattr with c_cflag CRTS_IFLOW
----------------------------------------------------------*/
JNIEXPORT jboolean JNICALL Java_gnu_io_I2CPort_isRTS( JNIEnv *env,
	jobject jobj )
{
	unsigned int result = 0;
	int fd = get_java_var( env, jobj,"fd","I" );

	ioctl( fd, TIOCMGET, &result );
	if( result & TIOCM_RTS ) return JNI_TRUE;
	else return JNI_FALSE;
}

/*----------------------------------------------------------
I2CPort.setRTS

   accept:      state  flag to set/unset.
   perform:     depends on the state flag
                if true TIOCM_RTS is set
                if false TIOCM_RTS is unset
   return:      none
   exceptions:  none
   comments:    tcsetattr with c_cflag CRTS_IFLOW
----------------------------------------------------------*/
JNIEXPORT void JNICALL Java_gnu_io_I2CPort_setRTS( JNIEnv *env,
	jobject jobj, jboolean state ) 
{
	unsigned int result = 0;
	int fd = get_java_var( env, jobj,"fd","I" );

	ioctl( fd, TIOCMGET, &result );
	if( state == JNI_TRUE ) result |= TIOCM_RTS;
	else result &= ~TIOCM_RTS;
	ioctl( fd, TIOCMSET, &result );
	return;
}

/*----------------------------------------------------------
I2CPort.setDSR

   accept:      state  flag to set/unset.
   perform:     depends on the state flag
                if true TIOCM_DSR is set
                if false TIOCM_DSR is unset
   return:      none
   exceptions:  none
   comments:    tcsetattr with c_cflag CRTS_IFLOW
----------------------------------------------------------*/
JNIEXPORT void JNICALL Java_gnu_io_I2CPort_setDSR( JNIEnv *env,
	jobject jobj, jboolean state ) 
{
	unsigned int result = 0;
	int fd = get_java_var( env, jobj,"fd","I" );

	ioctl( fd, TIOCMGET, &result );
	if( state == JNI_TRUE ) result |= TIOCM_DSR;
	else result &= ~TIOCM_DSR;
	ioctl( fd, TIOCMSET, &result );
	return;
}

/*----------------------------------------------------------
I2CPort.isDTR

   accept:      none
   perform:     check status of DTR
   return:      true if TIOCM_DTR is set
                false if TIOCM_DTR is not set
   exceptions:  none
   comments:    DTR stands for Data Terminal Ready
----------------------------------------------------------*/
JNIEXPORT jboolean JNICALL Java_gnu_io_I2CPort_isDTR( JNIEnv *env,
	jobject jobj )
{
	unsigned int result = 0;
	int fd = get_java_var( env, jobj,"fd","I" );

	ioctl( fd, TIOCMGET, &result );
	if( result & TIOCM_DTR ) return JNI_TRUE;
	else return JNI_FALSE;
}

/*----------------------------------------------------------
I2CPort.setDTR

   accept:      new DTR state
   perform:     if state is true, TIOCM_DTR is set
                if state is false, TIOCM_DTR is unset
   return:      none
   exceptions:  none
   comments:    DTR stands for Data Terminal Ready
----------------------------------------------------------*/
JNIEXPORT void JNICALL Java_gnu_io_I2CPort_setDTR( JNIEnv *env,
	jobject jobj, jboolean state )
{
	unsigned int result = 0;
	int fd = get_java_var( env, jobj,"fd","I" );

	ioctl( fd, TIOCMGET, &result );
	if( state == JNI_TRUE ) result |= TIOCM_DTR;
	else result &= ~TIOCM_DTR;
	ioctl( fd, TIOCMSET, &result );
	return;
}

/*----------------------------------------------------------
read_byte_array

   accept:      int                fd   file descriptor to read from
                unsigned char *buffer   buffer to read data into
                int            length   number of bytes to read
		int           timeout   milliseconds to wait before returning
   perform:     read bytes from the port into a buffer
   return:      status of read
                -1 fail (IOException)
                 0 timeout
                >0 number of bytes read
   comments:    According to the Communications API spec, a receive threshold
                of 1 is the same as having the threshold disabled.
		
		The nuts and bolts are documented in
		NativeEnableReceiveTimeoutThreshold()
----------------------------------------------------------*/ 
int read_byte_array( int fd, unsigned char *buffer, int length, int timeout )
{
	int ret, left, bytes = 0;
	fd_set rfds;
	struct timeval sleep;
	struct timeval *psleep=&sleep;

	left = length;
	FD_ZERO( &rfds );
	FD_SET( fd, &rfds );
	if( timeout != 0 )
	{
		sleep.tv_sec = timeout / 1000;
		sleep.tv_usec = 1000 * ( timeout % 1000 );
	}
	while( bytes < length ) 
	{
         /* FIXME: In Linux, select updates the timeout automatically, so
            other OSes will need to update it manually if they want to have
            the same behavior.  For those OSes, timeouts will occur after no
            data AT ALL is received for the timeout duration.  No big deal. */
		do {
			if( timeout == 0 ) psleep = NULL;
			ret=select( fd + 1, &rfds, NULL, NULL, psleep );
		}  while (ret < 0 && errno==EINTR);
		if( ret == 0 ) break;
		if( ret < 0 ) return -1;
		ret = read( fd, buffer + bytes, left );
		if( ret == 0 ) break;
		if( ret < 0 ) return -1;
		bytes += ret;
		left -= ret;
	}
	return bytes;
}

/*----------------------------------------------------------
NativeEnableReceiveTimeoutThreshold
   accept:      int  threshold, int vtime,int buffer
   perform:     Set c_cc->VMIN to threshold and c_cc=>VTIME to vtime
   return:      void
   exceptions:  IOException
   comments:    This is actually all handled in read with select in 
                canonical input mode.
----------------------------------------------------------*/ 
 
JNIEXPORT void JNICALL Java_gnu_io_I2CPort_NativeEnableReceiveTimeoutThreshold(JNIEnv *env, jobject jobj, jint vtime, jint threshold, jint buffer)
{
	int fd = get_java_var( env, jobj,"fd","I" );
	struct termios ttyset;

	if( tcgetattr( fd, &ttyset ) < 0 ) goto fail;
	ttyset.c_cc[ VMIN ] = threshold;
	ttyset.c_cc[ VTIME ] = vtime/100;
	if( tcsetattr( fd, TCSANOW, &ttyset ) < 0 ) goto fail;

	return;
fail:
	throw_java_exception( env, IO_EXCEPTION, "TimeoutThreshold", strerror( errno ) );
	return;
}

/*----------------------------------------------------------
I2CPort.readByte

   accept:      none
   perform:     Read a single byte from the port
   return:      The byte read
   exceptions:  IOException
----------------------------------------------------------*/ 
JNIEXPORT jint JNICALL Java_gnu_io_I2CPort_readByte( JNIEnv *env,
	jobject jobj )
{ 
	int bytes;
	unsigned char buffer[ 1 ];
	int fd = get_java_var( env, jobj,"fd","I" );
	int timeout = get_java_var( env, jobj, "timeout", "I" );

	bytes = read_byte_array( fd, buffer, 1, timeout );
	if( bytes < 0 ) {
		throw_java_exception( env, IO_EXCEPTION, "readByte",
			strerror( errno ) );
		return -1;
	}
	return (bytes ? (jint)buffer[ 0 ] : -1);
}

/*----------------------------------------------------------
I2CPort.readArray

   accept:       offset (offset to start storing data in the jbarray) and 
                 Length (bytes to read)
   perform:      read bytes from the port into a byte array
   return:       bytes read on success
                 0 on read timeout
   exceptions:   IOException
   comments:     throws ArrayIndexOutOfBoundsException if asked to
                 read more than SSIZE_MAX bytes
----------------------------------------------------------*/ 
JNIEXPORT jint JNICALL Java_gnu_io_I2CPort_readArray( JNIEnv *env,
	jobject jobj, jbyteArray jbarray, jint offset, jint length )
{  
	int bytes;
	jbyte *body;
	unsigned char *buffer;
	int fd = get_java_var( env, jobj, "fd", "I" );
	int timeout = get_java_var( env, jobj, "timeout", "I" );

	if( (size_t) length > SSIZE_MAX || length < 0 ) {
		throw_java_exception( env, ARRAY_INDEX_OUT_OF_BOUNDS,
			"readArray", "Invalid length" );
		return -1;
	}

	buffer = (unsigned char *)malloc( sizeof( unsigned char ) * length );
	if( buffer == 0 ) {
		throw_java_exception( env, OUT_OF_MEMORY, "readArray",
			"Unable to allocate buffer" );
		return -1;
	}

	bytes = read_byte_array( fd, buffer, length, timeout );
	if( bytes < 0 ) {
		free( buffer );
		throw_java_exception( env, IO_EXCEPTION, "readArray",
			strerror( errno ) );
		return -1;
	}
	body = (*env)->GetByteArrayElements( env, jbarray, 0 );
	memcpy(body + offset, buffer, bytes);
	(*env)->ReleaseByteArrayElements( env, jbarray, body, 0 );
	free( buffer );
	return (bytes ? bytes : -1);
}

/*----------------------------------------------------------
I2CPort.nativeavailable

   accept:      none
   perform:     find out the number of bytes available for reading
   return:      available bytes
                -1 on error
   exceptions:  none
----------------------------------------------------------*/ 
JNIEXPORT jint JNICALL Java_gnu_io_I2CPort_nativeavailable( JNIEnv *env,
	jobject jobj )
{
	int fd = get_java_var( env, jobj,"fd","I" );
	int result;

	if( ioctl( fd, FIONREAD, &result ) ) 
	{
		throw_java_exception( env, IO_EXCEPTION, "nativeavailable", strerror( errno ) );
		return -1;
	}
	else return (jint)result;

}

/*----------------------------------------------------------
I2CPort.setflowcontrol

   accept:      flowmode 
	FLOWCONTROL_NONE        none
	FLOWCONTROL_RTSCTS_IN   hardware flow control
	FLOWCONTROL_RTSCTS_OUT         ""
	FLOWCONTROL_XONXOFF_IN  input software flow control
	FLOWCONTROL_XONXOFF_OUT output software flow control
   perform:     set flow control to flowmode
   return:      none
   exceptions:  IOException
   comments:  there is no differentiation between input and output hardware
              flow control
----------------------------------------------------------*/
JNIEXPORT void JNICALL Java_gnu_io_I2CPort_setflowcontrol( JNIEnv *env,
	jobject jobj, jint flowmode )
{
	struct termios ttyset;
	int fd = get_java_var( env, jobj,"fd","I" );

	if( tcgetattr( fd, &ttyset ) ) goto fail;
	
	if ( flowmode & ( FLOWCONTROL_RTSCTS_IN | FLOWCONTROL_RTSCTS_OUT ) )
		ttyset.c_cflag |= HARDWARE_FLOW_CONTROL;
	else ttyset.c_cflag &= ~HARDWARE_FLOW_CONTROL;

	ttyset.c_iflag &= ~IXANY;

	if ( flowmode & FLOWCONTROL_XONXOFF_IN )
		ttyset.c_iflag |= IXOFF;
	else ttyset.c_iflag &= ~IXOFF;

	if ( flowmode & FLOWCONTROL_XONXOFF_OUT )
		ttyset.c_iflag |= IXON;
	else ttyset.c_iflag &= ~IXON;

	if( tcsetattr( fd, TCSANOW, &ttyset ) ) goto fail;
	return;
fail:
	throw_java_exception( env, IO_EXCEPTION, "setHWFC",
		strerror( errno ) );
	return;
}

/*----------------------------------------------------------
I2CPort.eventLoop

   accept:      none
   perform:     periodically check for I2CPortEvents
   return:      none
   exceptions:  none
   comments:    FIXME This is probably wrong on bsd.
----------------------------------------------------------*/ 
JNIEXPORT void JNICALL Java_gnu_io_I2CPort_eventLoop( JNIEnv *env,
	jobject jobj )
{
	int fd, ret, change;
	fd_set rfds;
	struct timeval tv_sleep;
	unsigned int mflags;
#if defined(TIOCGICOUNT)
	struct serial_icounter_struct sis, osis;
#endif /* TIOCGICOUNT */
	unsigned int omflags;

	jmethodID method, interrupt;
	jboolean interrupted = 0;
	jclass jclazz, jthread;
	jclazz = (*env)->GetObjectClass( env, jobj );
	fd = get_java_var(env, jobj, "fd", "I");
	method = (*env)->GetMethodID( env, jclazz, "sendEvent", "(IZ)V" );
	jthread = (*env)->FindClass( env, "java/lang/Thread" );
	interrupt = (*env)->GetStaticMethodID( env, jthread, "interrupted", "()Z" );

	/* Some multiport i2c cards do not implement TIOCGICOUNT ... */
#if defined(TIOCGICOUNT)
	if( ioctl( fd, TIOCGICOUNT, &osis ) < 0 ) {
		fprintf( stderr, "Port does not support TIOCGICOUNT events\n" );
		return; 
	}
#else
	fprintf( stderr, "Port does not support all Hardware events\n" );
#endif /*  TIOCGICOUNT */

	if( ioctl( fd, TIOCMGET, &omflags) <0 ) {
		fprintf( stderr, "Port does not support events\n" );
 		return;
	}

	FD_ZERO( &rfds );
	while( !interrupted ) {
		FD_SET( fd, &rfds );
		/* Check every 1 second, or on receive data */
		tv_sleep.tv_sec = 1; 
		tv_sleep.tv_usec = 0;
		do {
			ret=select( fd + 1, &rfds, NULL, NULL, &tv_sleep );
		}  while (ret < 0 && errno==EINTR);
		if( ret < 0 ) {
			fprintf( stderr, "select() Failed\n" );
			break; 
		}

#if defined TIOCSERGETLSR
		if( ioctl( fd, TIOCSERGETLSR, &change ) ) {
			fprintf( stderr, "TIOCSERGETLSR Failed\n" );
			break;
		}
		else if( change ) {
			(*env)->CallVoidMethod( env, jobj, method,
				(jint)SPE_OUTPUT_BUFFER_EMPTY, JNI_TRUE );
		}
#endif /* TIOCSERGETLSR */
#if defined(TIOCGICOUNT)
	/*	wait for RNG, DSR, CD or CTS  but not DataAvailable
	 *      The drawback here is it never times out so if someone
	 *      reads there will be no chance to try again.
	 *      This may make sense if the program does not want to 
	 *      be notified of data available or errors.
	 *	ret=ioctl(fd,TIOCMIWAIT);
	 */
		if( ioctl( fd, TIOCGICOUNT, &sis ) ) {
			fprintf( stderr, "TIOCGICOUNT Failed\n" );
			break; 
		}
		while( sis.frame != osis.frame ) {
			(*env)->CallVoidMethod( env, jobj, method, (jint)SPE_FE, JNI_TRUE );
			osis.frame++;
		}
		while( sis.overrun != osis.overrun ) {
			(*env)->CallVoidMethod( env, jobj, method, (jint)SPE_OE, JNI_TRUE );
			osis.overrun++;
		}
		while( sis.parity != osis.parity ) {
			(*env)->CallVoidMethod( env, jobj, method, (jint)SPE_PE, JNI_TRUE );
			osis.parity++;
		}
		while( sis.brk != osis.brk ) {
			(*env)->CallVoidMethod( env, jobj, method, (jint)SPE_BI, JNI_TRUE );
			osis.brk++;
		}
		osis = sis;
#endif /*  TIOCGICOUNT */
		if( ioctl( fd, TIOCMGET, &mflags ) ) {
			fprintf( stderr, "TIOCMGET Failed\n" );
			break; 
		}
		interrupted = (*env)->CallStaticBooleanMethod( env, jthread, interrupt );
	       /* A Portable implementation */
		change = (mflags&TIOCM_CTS) - (omflags&TIOCM_CTS);
		if( change ) {
			fprintf(stderr, "Sending SPE_CTS\n");
			(*env)->CallVoidMethod( env, jobj, method,
				(jint)SPE_CTS, JNI_TRUE );
		}
		change = (mflags&TIOCM_DSR) - (omflags&TIOCM_DSR);
		if( change ) {
			fprintf(stderr, "Sending SPE_DSR\n");
			(*env)->CallVoidMethod( env, jobj, method,
				(jint)SPE_DSR, JNI_TRUE );
		}
		change = (mflags&TIOCM_RNG) - (omflags&TIOCM_RNG);
		if( change ) {
			fprintf(stderr, "Sending SPE_RI\n");
			(*env)->CallVoidMethod( env, jobj, method,
				(jint)SPE_RI, JNI_TRUE );
		}
		change = (mflags&TIOCM_CD) - (omflags&TIOCM_CD);
		if( change ) {
			fprintf(stderr, "Sending SPE_CD\n");
			(*env)->CallVoidMethod( env, jobj, method,
				(jint)SPE_CD, JNI_TRUE );
		}
		omflags = mflags;
		if( ioctl( fd, FIONREAD, &change ) ) {
			fprintf( stderr, "FIONREAD Failed\n" );
		}
		else if( change ) {
			(*env)->CallVoidMethod( env, jobj, method,
				(jint)SPE_DATA_AVAILABLE, JNI_TRUE );
			usleep(1000); /* select wont block */
		}
	}
	return;
}

/*----------------------------------------------------------
 send_modem_events

   accept:      int    event     I2CPortEvent constant
                int    change    Number of times this event happened
                int    state     current state: 0 is false, nonzero is true
   perform:     Send the necessary events
   return:      none
   exceptions:  none
   comments:    Since the interrupt counters tell us how many times the
                state has changed, we can send a I2CPortEvent for each
                interrupt (change) that has occured.  If we don't do this,
                we'll miss a whole bunch of events.
----------------------------------------------------------*/ 
void send_modem_events( JNIEnv *env, jobject jobj, jmethodID method,
	int event, int change, int state )
{
	int i, s;
	jboolean flag;
	if( state ) s = 1;
	else s = 0;

	for( i = 0; i < change; i++ ) {
		if( ( change + s + i ) % 2 ) flag = JNI_FALSE;
		else flag = JNI_TRUE;
		(*env)->CallVoidMethod( env, jobj, method, (jint)event, flag );
	}
}

/*----------------------------------------------------------
get_java_fd

   accept:      env (keyhole to java)
                jobj (java I2CPort object)
   return:      the fd field from the java object
   exceptions:  none
   comments:
----------------------------------------------------------*/ 
int get_java_var( JNIEnv *env, jobject jobj, char *id, char *type )
{
	int result = 0;
	jclass jclazz = (*env)->GetObjectClass( env, jobj );
	jfieldID jfd = (*env)->GetFieldID( env, jclazz, id, type );
	if( !jfd ) {
		(*env)->ExceptionDescribe( env );
		(*env)->ExceptionClear( env );
		return result;
	}
	result = (int)( (*env)->GetIntField( env, jobj, jfd ) );
/* ct7 & gel * Added DeleteLocalRef */
	(*env)->DeleteLocalRef( env, jclazz );
	return result;
}

/*----------------------------------------------------------
throw_java_exception

   accept:      env (keyhole to java)
                *exc (exception class name)
                *foo (function name)
                *msg (error message)
   perform:     Throw a new java exception
   return:      none
   exceptions:  haha!
   comments:
----------------------------------------------------------*/ 
void throw_java_exception( JNIEnv *env, char *exc, char *foo, char *msg )
{
	char buf[ 60 ];
	jclass clazz = (*env)->FindClass( env, exc );
	if( !clazz ) {
		(*env)->ExceptionDescribe( env );
		(*env)->ExceptionClear( env );
		return;
	}
#if defined(_GNU_SOURCE)
	snprintf( buf, 60, "%s in %s", msg, foo );
#else
	sprintf( buf,"%s in %s", msg, foo );
#endif /* _GNU_SOURCE */
	(*env)->ThrowNew( env, clazz, buf );
/* ct7 * Added DeleteLocalRef */
	(*env)->DeleteLocalRef( env, clazz );
}

JNIEXPORT jboolean  JNICALL Java_gnu_io_RXTXCommDriver_IsDeviceGood(JNIEnv *env,
	jobject jobj, jstring tty_name){

	jboolean result;
	static struct stat mystat;
	char teststring[256];
	int fd,i;
    	const char *name = (*env)->GetStringUTFChars(env, tty_name, 0);

#if defined(__linux__)
	if(!strcmp(name,"tty0")|| !strcmp(name,"ttyd")||
		!strcmp(name,"ttyq")|| !strcmp(name,"ttym")||
		!strcmp(name,"ttyf")|| !strcmp(name,"cuaa")
		)
	{
#ifdef DEBUG
		fprintf(stderr,"DEBUG: Ignoring Port %s\*\n",name);
#endif
		return(JNI_FALSE);
	}
#endif
#if defined(__FreeBSD__)
	if(!strcmp(name,"tty0")|| !strcmp(name,"ttyd")||
		!strcmp(name,"ttyq")|| !strcmp(name,"ttym")||
		!strcmp(name,"ttyf")|| !strcmp(name,"ttyS")||
		!strcmp(name,"ttyI")|| !strcmp(name,"ttyW")||
		!strcmp(name,"ttyC")|| !strcmp(name,"ttyR")
		)
	{
#ifdef DEBUG
		fprintf(stderr,"DEBUG: Ignoring Port %s*\n",name);
#endif
		return(JNI_FALSE);
	}
#endif
#if defined(__NetBSD__)
	if(     !strcmp(name,"ttyd")||
		!strcmp(name,"ttyq")|| !strcmp(name,"ttym")||
		!strcmp(name,"ttyf")|| !strcmp(name,"ttyS")||
		!strcmp(name,"ttyI")|| !strcmp(name,"ttyW")||
		!strcmp(name,"ttyq")|| !strcmp(name,"ttym")||
		!strcmp(name,"ttyf")|| !strcmp(name,"cuaa")||
		!strcmp(name,"ttyC")|| !strcmp(name,"ttyR")||
		!strcmp(name,"ttyM")
		)
	{
#ifdef DEBUG
		fprintf(stderr,"DEBUG: Ignoring Port %s*\n",name);
#endif
		return(JNI_FALSE);
	}
#endif
	for(i=0;i<64;i++){
		sprintf(teststring,"/dev/%s%i",name, i);
		stat(teststring,&mystat);
		if(S_ISCHR(mystat.st_mode)){
			fd=open(teststring,O_RDONLY|O_NONBLOCK);
			if (fd>0){
				close(fd);
				result=JNI_TRUE;
				break;
			}
			result=JNI_FALSE;
		}
		else result=JNI_FALSE;
	}
	sprintf(teststring,"/dev/%s",name);
	stat(teststring,&mystat);
	if(S_ISCHR(mystat.st_mode)){
		fd=open(teststring,O_RDONLY|O_NONBLOCK);
		if (fd>0){
			close(fd);
			result=JNI_TRUE;
		}
	}
	(*env)->ReleaseStringUTFChars(env, tty_name, name);
	return(result);
}
JNIEXPORT void JNICALL Java_gnu_io_I2CPort_setInputBufferSize(JNIEnv *env, jobject jobj,  jint size )
{
#ifdef DEBUG
	fprintf(stderr,"setInputBufferSize is not implemented\n");
#endif
}
JNIEXPORT jint JNICALL Java_gnu_io_I2CPort_getInputBufferSize(JNIEnv *env, jobject jobj)
{
#ifdef DEBUG
	fprintf(stderr,"getInputBufferSize is not implemented\n");
#endif
	return(1);
}
JNIEXPORT void JNICALL Java_gnu_io_I2CPort_setOutputBufferSize(JNIEnv *env, jobject jobj, jint size )
{
#ifdef DEBUG
	fprintf(stderr,"setOutputBufferSize is not implemented\n");
#endif
}
JNIEXPORT jint JNICALL Java_gnu_io_I2CPort_getOutputBufferSize(JNIEnv *env, jobject jobj)
{
#ifdef DEBUG
	fprintf(stderr,"getOutputBufferSize is not implemented\n");
#endif
	return(1);
}

void dump_termios(char *foo,struct termios *ttyset)
{
	int i;

	fprintf(stderr,"%s %o\n",foo,ttyset->c_iflag);
	fprintf(stderr,"%s %o\n",foo,ttyset->c_lflag);
	fprintf(stderr,"%s %o\n",foo,ttyset->c_oflag);
	fprintf(stderr,"%s %o\n",foo,ttyset->c_cflag);
	for(i=0;i<NCCS;i++)
	{
		fprintf(stderr,"%s %o ",foo,ttyset->c_cc[i]);
	}
	fprintf(stderr,"\n");
}
