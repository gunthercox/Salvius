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

import com.xuggle.xuggler.io.IURLProtocolHandler;

/**
 * Used by URLProtocolManager to get a factory for a given protocol.
 * 
 * Implement this interface on any factories that make your
 * specific implementation of IURLProtocolHandler, and then
 * register the factory with your URLProtocolManager
 */
public interface IURLProtocolHandlerFactory
{
  /**
   * Called by FFMPEG in order to get a handler to use for a given file.
   * 
   * @param protocol The protocol without a ':'.  For example, "file", "http", or "yourcustomprotocol"
   * @param url The URL that FFMPEG is trying to open.
   * @param flags The flags that FFMPEG will pass to {@link IURLProtocolHandler#open(String, int)}
   * @return A {@link IURLProtocolHandler} to use, or null.  If null, a file not found error will be passed back
   *   to FFMPEG.
   */
  public IURLProtocolHandler getHandler(String protocol, String url,
      int flags);
}
