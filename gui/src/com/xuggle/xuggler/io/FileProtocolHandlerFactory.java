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

package com.xuggle.xuggler.io;

import com.xuggle.xuggler.io.FileProtocolHandler;
import com.xuggle.xuggler.io.IURLProtocolHandler;
import com.xuggle.xuggler.io.IURLProtocolHandlerFactory;


/**
 * Implementation of {@link IURLProtocolHandlerFactory} that demonstrates how
 * you can have Java act just like FFMPEG's internal "file:" protocol.
 *  
 * This just duplicates all the functionality in the default "file:" protocol
 * that FFMPEG implemements, but demonstrates how you can have FFMPEG
 * call back into Java.
 * 
 */
public class FileProtocolHandlerFactory implements
    IURLProtocolHandlerFactory
{
  public IURLProtocolHandler getHandler(String protocol, String url,
      int flags)
  {
    return new FileProtocolHandler(url);
  }

}
