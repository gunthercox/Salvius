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

package com.xuggle.mediatool;

import java.util.Collection;

/**
 * Generates events that {@link IMediaListener} objects can
 * subscribe to and react to.
 * <p>
 * This is the interface that defines how you
 * {@link #addListener(IMediaListener)} s and
 * {@link #removeListener(IMediaListener)}s from different
 * {@link IMediaGenerator} objects such as {@link IMediaReader}.
 * 
 * </p>
 */

public interface IMediaGenerator
{
  /**
   * Add a media tool listener.
   *
   * @param listener the listener to add
   *
   * @return true if the set of listeners changed as a result of the call
   */
  
  public abstract boolean addListener(IMediaListener listener);
  
  /**
   * Remove a media tool listener.
   *
   * @param listener the listener to remove
   *
   * @return true if the set of listeners changed as a result of the call
   */
  
  public abstract boolean removeListener(IMediaListener listener);
  
  /**
   * Get the list of existing media tools listeners.
   *
   * @return an unmodifiable collection of listeners
   */
  
  public abstract Collection<IMediaListener> getListeners();
  

}
