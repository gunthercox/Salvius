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

import com.xuggle.xuggler.io.FfmpegIO;
import com.xuggle.xuggler.io.FfmpegIOHandle;

/**
 * For Internal Use Only.
 * 
 * This class only exists to help tests in other packages run
 * the FFMPEG IO functions.
 * <p>
 * Normal classes don't have access to these mechanisms, but we
 * expose them here.
 * </p>
 */
public class Helper
{
  public static int url_open(FfmpegIOHandle handle, String filename,
      int flags)
  {
    return FfmpegIO.url_open(handle, filename, flags);
  }

  public static int url_read(FfmpegIOHandle handle, byte[] buffer,
      int length)
  {
    return FfmpegIO.url_read(handle, buffer, length);
  }

  public static int url_close(FfmpegIOHandle handle)
  {
    return FfmpegIO.url_close(handle);
  }

  public static int url_write(FfmpegIOHandle handle, byte[] buffer,
      int length)
  {
    return FfmpegIO.url_write(handle, buffer, length);
  }

  public static long url_seek(FfmpegIOHandle handle, long position,
      int whence)
  {
    return FfmpegIO.url_seek(handle, position, whence);
  }
}
