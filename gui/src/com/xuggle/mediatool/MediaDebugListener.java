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

import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentMap;
import java.util.concurrent.atomic.AtomicLong;


import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.xuggle.mediatool.IMediaListener;
import com.xuggle.mediatool.IMediaGenerator;
import com.xuggle.mediatool.event.IAddStreamEvent;
import com.xuggle.mediatool.event.IAudioSamplesEvent;
import com.xuggle.mediatool.event.ICloseCoderEvent;
import com.xuggle.mediatool.event.ICloseEvent;
import com.xuggle.mediatool.event.IFlushEvent;
import com.xuggle.mediatool.event.IOpenCoderEvent;
import com.xuggle.mediatool.event.IOpenEvent;
import com.xuggle.mediatool.event.IReadPacketEvent;
import com.xuggle.mediatool.event.IVideoPictureEvent;
import com.xuggle.mediatool.event.IWriteHeaderEvent;
import com.xuggle.mediatool.event.IWritePacketEvent;
import com.xuggle.mediatool.event.IWriteTrailerEvent;

import static com.xuggle.mediatool.IMediaDebugListener.Event.*;
import static com.xuggle.mediatool.IMediaDebugListener.Mode.*;

/**
 * An {@link IMediaListener} that counts {@link IMediaGenerator}
 * events and optionally logs the events specified in {@link MediaDebugListener.Event}.
 * <p>
 * This object can be handy for debugging a media listener to see when
 * and where events are occurring.
 * </p>
 * <p>
 * AEventMixin counts can be queried, and {@link #toString} will
 * return an event count summary.  The details in the log can be
 * controlled by {@link MediaDebugListener.Mode}.
 * </p>
 * <p>
 * A {@link MediaDebugListener} can be attached to multiple {@link IMediaGenerator}
 * simultaneously, even if they are on different threads, in which case
 * it will return aggregate counts.
 * </p>
 */

class MediaDebugListener extends MediaListenerAdapter implements IMediaDebugListener
{
  final private Logger log = LoggerFactory.getLogger(this.getClass());
  // update max name length

  // max event name length
  private static final int mMaxNameLength;
  static {
    int maxNameLen = 0;
    for (Event event : Event.values())
      maxNameLen = Math.max(event.name().length(), maxNameLen);
    mMaxNameLength = maxNameLen;
  }
  
  /**
   * Get the maximum length of an event name.
   * @return the maximum length.
   */

  private static int getMaxNameLength()
  {
    return mMaxNameLength;
  }
  
  
  // log modes

  // the flags
  
  volatile private int mFlags;
  
  // log mode

  volatile private Mode mMode;

  // the event counts
  
  final private ConcurrentMap<Event, AtomicLong> mEventCounts = 
    new ConcurrentHashMap<Event, AtomicLong>();

  // the symbolic name of this listener
  
  private final String mName;

  /** 
   * Construct a debug listener which logs all event types.
   */

  MediaDebugListener()
  {
    this(PARAMETERS, ALL);
  }

  /** 
   * Construct a debug listener with custom set of event types to log.
   *
   * @param events the event types which will be logged
   */
  
  MediaDebugListener(Event... events)
  {
    this(PARAMETERS, events);
  }

  /** 
   * Construct a debug listener with custom set of event types to log.
   *
   * @param mode log mode, see {@link MediaDebugListener.Mode}
   * @param events the event types which will be logged
   */
  
  MediaDebugListener(Mode mode, Event... events)
  {
    this(null, mode, events);
  }

  /**
   * Construct a debug listener with custom name and set of event types to
   * log.
   * 
   * @param name symbolic name for this debug listener
   * @param mode log mode, see {@link MediaDebugListener.Mode}
   * @param events the event types which will be logged
   */

  MediaDebugListener(String name, Mode mode, Event... events)
  {
    mName = name;
    mMode = mode;
    setLogEvents(events);
  }
  
  
  // increment count for specific event type

  private void incrementCount(Event event)
  {
    for (Event candidate: Event.values())
      if ((candidate.getFlag() & event.getFlag()) != 0)
      {
        AtomicLong newValue = new AtomicLong(0);
        AtomicLong count = mEventCounts.putIfAbsent(candidate, newValue);
        if (count == null)
          count = newValue;
        count.incrementAndGet();
      }
  }

  /** 
   * Get the current count of events of a particular type.
   *
   * @param event the specified event type
   * 
   * @return the number of events of the specified type which have been
   *         transpired
   */

  public long getCount(Event event)
  {
    AtomicLong value = mEventCounts.get(event);
    return (null == value) ? 0 : value.get();
  }

  /** 
   * Reset all the event counts.
   */

  public void resetCounts()
  {
    mEventCounts.clear();
  }

  /** 
   * Set the event types which will be logged.
   *
   * @param events the events which will be logged
   */

  public void setLogEvents(Event... events)
  {
    mFlags = 0;
    for (Event event: events)
      mFlags |= event.getFlag();
  }

  /** 
   * Get the flags which specify which events will be logged.
   * 
   * @return the flags.
   */

  public int getFlags()
  {
    return mFlags;
  }

  // handle an event 

  private void handleEvent(Event event, IMediaGenerator tool, Object... args)
  {
    incrementCount(event);
    if ((mFlags & event.getFlag()) != 0 && mMode != NOTHING)
    {
      StringBuilder string = new StringBuilder();
      if (mName != null)
        string.append(mName + " ");
      
      string.append(event.getMethod() + "(");
      switch (mMode)
      {
      case URL:
        if (tool instanceof IMediaCoder)
          string.append(((IMediaCoder)tool).getUrl());
        break;
      case PARAMETERS:
        for (Object arg: args)
          string.append(arg + (arg == args[args.length - 1] ? "" : ", "));
        break;
      }
      string.append(")");
      log.debug(string.toString());
    }
  }

  /** {@inheritDoc} */

  public void onVideoPicture(IVideoPictureEvent event)
  {
    handleEvent(VIDEO, event.getSource(), new Object[] {event.getPicture(),
        event.getImage(),
        event.getStreamIndex()});
  }
  
  /** {@inheritDoc} */

  public void onAudioSamples(IAudioSamplesEvent event)
  {
    handleEvent(AUDIO, event.getSource(), new Object[] {
        event.getAudioSamples(),
        event.getStreamIndex()});
  }
  
  /** {@inheritDoc} */

  public void onOpen(IOpenEvent event)
  {
    handleEvent(OPEN, event.getSource(), new Object[] {});
  }
  
  /** {@inheritDoc} */

  public void onClose(ICloseEvent event)
  {
    handleEvent(CLOSE, event.getSource(), new Object[] {});
  }
  
  /** {@inheritDoc} */

  public void onAddStream(IAddStreamEvent event)
  {
    handleEvent(ADD_STREAM, event.getSource(),
        new Object[] {event.getStreamIndex()});
  }
  
  /** {@inheritDoc} */

  public void onOpenCoder(IOpenCoderEvent event)
  {
    handleEvent(OPEN_STREAM, event.getSource(),
        new Object[] {event.getStreamIndex()});
  }
  
  /** {@inheritDoc} */

  public void onCloseCoder(ICloseCoderEvent event)
  {
    handleEvent(CLOSE_STREAM, event.getSource(),
        new Object[] {event.getStreamIndex()});
  }
  
  /** {@inheritDoc} */

  public void onReadPacket(IReadPacketEvent event)
  {
    handleEvent(READ_PACKET, event.getSource(),
        new Object[] {event.getPacket()});
  }
  
  /** {@inheritDoc} */

  public void onWritePacket(IWritePacketEvent event)
  {
    handleEvent(WRITE_PACKET, event.getSource(),
        new Object[] {event.getPacket()});
  }

  /** {@inheritDoc} */

  public void onWriteHeader(IWriteHeaderEvent event)
  {
    handleEvent(HEADER, event.getSource(), new Object[] {});
  }
  
  /** {@inheritDoc} */

  public void onFlush(IFlushEvent event)
  {
    handleEvent(FLUSH, event.getSource(), new Object[] {});
  }

  /** {@inheritDoc} */

  public void onWriteTrailer(IWriteTrailerEvent event)
  {
    handleEvent(TRAILER, event.getSource(), new Object[] {});
  }

  /** {@inheritDoc}
   * Returns a string with event counts formatted nicely.
   * @return a formatted string.
   */

  public String toString()
  {
    StringBuilder sb = new StringBuilder();
    
    sb.append("event counts: ");
    for (Event event: Event.values())
      sb.append(String.format("\n  %" + getMaxNameLength() + "s: %d",
          event.name(), getCount(event)));

    return sb.toString();
  }

}
