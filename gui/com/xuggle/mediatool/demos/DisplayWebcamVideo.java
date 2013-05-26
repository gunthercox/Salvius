/*******************************************************************************
 * Copyright (c) 2008, 2010 Xuggle Inc.  All rights reserved.
 *  
 * This file is part of Xuggle-Xuggler-Main.
 *
 * Xuggle-Xuggler-Main is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Xuggle-Xuggler-Main is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with Xuggle-Xuggler-Main.  If not, see <http://www.gnu.org/licenses/>.
 *******************************************************************************/

package com.xuggle.mediatool.demos;

import javax.swing.JFrame;

import com.xuggle.mediatool.IMediaReader;
import com.xuggle.mediatool.ToolFactory;
import com.xuggle.xuggler.IError;
import com.xuggle.xuggler.IMetaData;
import com.xuggle.xuggler.IContainer;
import com.xuggle.xuggler.IContainerFormat;


/**
 * Using {@link IMediaReader}, takes a FFMPEG device driver name (ex:
 * "video4linux2"), and a device name (ex: /dev/video0), and displays
 * video from that device.  For example, a web camera.
 * 
 * <p> For example, to play the default camera on these operating
 * systems: <ul> <li>Microsoft Windows:<pre>java -cp
 * %XUGGLE_HOME%\share\java\jars\xuggle-xuggler.jar
 * com.xuggle.mediatool.demos.DisplayWebcamVideo vfwcap 0</pre></li>
 * <li>Linux:<pre>java -cp
 * $XUGGLE_HOME/share/java/jars/xuggle-xuggler.jar
 * com.xuggle.mediatool.demos.DisplayWebcamVideo video4linux2
 * /dev/video0</pre></li> </ul> </p>
 * 
 * @author aclarke
 * @author trebor
 */

public class DisplayWebcamVideo
{
  /**
   * Takes a FFMPEG webcam driver name, and a device name, opens the
   * webcam, and displays its video in a Swing window.
   * <p>
   * Examples of device formats are:
   * </p>
   * <table border="1">
   * <thead>
   *  <tr>
   *  <td>OS</td>
   *  <td>Driver Name</td>
   *  <td>Sample Device Name</td>
   *  </tr>
   *  </thead>
   *  <tbody>
   *  <tr>
   *  <td>Windows</td>
   *  <td>vfwcap</td>
   *  <td>0</td>
   *  </tr>
   *  <tr>
   *  <td>Linux</td>
   *  <td>video4linux2</td>
   *  <td>/dev/video0</td>
   *  </tr>
   *  </tbody>
   *  </table>
   * 
   * <p>
   * Webcam support is very limited; you can't query what devices are
   * available, nor can you query what their capabilities are without
   * actually opening the device.  Sorry, but that's how FFMPEG rolls.
   * </p>
   * 
   * @param args Must contain two strings: a FFMPEG driver name and a
   *   device name (which is dependent on the FFMPEG driver).
   */

  public static void main(String[] args)
  {
    if (args.length != 2)
      throw new IllegalArgumentException(
        "must pass in a driver name and a device name");
    
    // create a new mr. display webcam video
    
    new DisplayWebcamVideo(args[0], args[1]);
  }

  /** Construct a DisplayWebcamVideo which reads and plays a video
   * from an attached webcam.
   * 
   * @param driverName the name of the webcan drive
   * @param deviceName the name of the webcan device
   */

  public DisplayWebcamVideo(String driverName, String deviceName)
  {
    // create a Xuggler container object

    IContainer container = IContainer.make();

    // tell Xuggler about the device format

    IContainerFormat format = IContainerFormat.make();
    if (format.setInputFormat(driverName) < 0)
      throw new IllegalArgumentException(
        "couldn't open webcam device: " + driverName);
    
    // devices, unlike most files, need to have parameters set in order
    // for Xuggler to know how to configure them, for a webcam, these
    // parameters make sense

    IMetaData params = IMetaData.make();
    
    params.setValue("framerate", "30/1");
    params.setValue("video_size", "320x240");
    
    // open the container

    int retval = container.open(deviceName, IContainer.Type.READ, format,
        false, true, params, null);
    if (retval < 0)
    {
      // this little trick converts the non friendly integer return
      // value into a slightly more friendly object to get a
      // human-readable error name

      IError error = IError.make(retval);
      throw new IllegalArgumentException(
        "could not open file: " + deviceName + "; Error: " + 
        error.getDescription());
    }      

    // create a media reader to wrap that container

    IMediaReader reader = ToolFactory.makeReader(container);
    
    // Add a media viewer that will display the video, but that exits
    // the JVM when it is destroyed
    reader.addListener(ToolFactory.makeViewer(true, JFrame.EXIT_ON_CLOSE));

    // read out the contents of the media file, note that nothing else
    // happens here.  action happens in the onVideoPicture() method
    // which is called when complete video pictures are extracted from
    // the media source.  Since we're reading from a web cam this
    // loop will never return, but if the window is closed, the JVM is
    // exited.

    while (reader.readPacket() == null)
      do {} while(false);

  }

}
