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

/**
 * Events that can be fired by the <code>com.xuggle.mediatool</code> package.
 * 
 * {@link com.xuggle.mediatool.event.IEvent} is the top of the interface
 * inheritance tree. If a given interface is instantiable as an event, you will
 * find a class with the same name without the starting &quot;I&quot;
 * <p>
 * Mixin classes (e.g. {@link com.xuggle.mediatool.event.AEventMixin}) are
 * provided as abstract classes implementing all the methods implied by their
 * name, but not actually declaring the interface. In this way child classes can
 * extend them, but separately decide which functionality to admit they have to
 * the outside world.
 * </p>
 */
package com.xuggle.mediatool.event;