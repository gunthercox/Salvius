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

import java.util.List;
import java.util.Map;
import java.util.Vector;
import java.util.HashMap;
import java.util.Collection;
import java.util.concurrent.TimeUnit;

import java.awt.image.BufferedImage;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.xuggle.mediatool.MediaReader;
import com.xuggle.mediatool.event.AddStreamEvent;
import com.xuggle.mediatool.event.AudioSamplesEvent;
import com.xuggle.mediatool.event.CloseCoderEvent;
import com.xuggle.mediatool.event.CloseEvent;
import com.xuggle.mediatool.event.FlushEvent;
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
import com.xuggle.mediatool.event.OpenCoderEvent;
import com.xuggle.mediatool.event.OpenEvent;
import com.xuggle.mediatool.event.VideoPictureEvent;
import com.xuggle.mediatool.event.WriteHeaderEvent;
import com.xuggle.mediatool.event.WritePacketEvent;
import com.xuggle.mediatool.event.WriteTrailerEvent;
import com.xuggle.xuggler.Global;
import com.xuggle.xuggler.ICodec;
import com.xuggle.xuggler.IError;
import com.xuggle.xuggler.IPacket;
import com.xuggle.xuggler.IStream;
import com.xuggle.xuggler.IRational;
import com.xuggle.xuggler.IContainer;
import com.xuggle.xuggler.IPixelFormat;
import com.xuggle.xuggler.IStreamCoder;
import com.xuggle.xuggler.IVideoPicture;
import com.xuggle.xuggler.IAudioSamples;
import com.xuggle.xuggler.IContainerFormat;
import com.xuggle.xuggler.video.IConverter;
import com.xuggle.xuggler.video.ConverterFactory;

import static com.xuggle.xuggler.ICodec.Type.CODEC_TYPE_VIDEO;
import static com.xuggle.xuggler.ICodec.Type.CODEC_TYPE_AUDIO;

import static java.util.concurrent.TimeUnit.MICROSECONDS;

/**
 * An {@link IMediaCoder} that encodes and decodes media to containers.
 * 
 * <p>
 * 
 * The MediaWriter class is a simplified interface to the Xuggler
 * library that opens up a media container, and allows media data to be
 * written into it.
 * 
 * </p>
 * 
 * <p>
 * The {@link MediaWriter} class implements {@link IMediaListener}, and so
 * it can be attached to any {@link IMediaGenerator} that generates raw
 * media events (e.g. {@link MediaReader}).
 * </p>
 * 
 * <p>
 * 
 * Calls to {@link #onAudioSamples}, and {@link #onVideoPicture} encode
 * media into packets and write those encoded packets.
 * 
 * </p>
 * <p>
 * 
 * If you are generating video from Java {@link BufferedImage} but you
 * don't have an {@link IVideoPicture} object handy, don't sweat.  You
 * can use {@link #pushImage(BufferedImage, int, long)}, and {@link MediaWriter}
 * will convert your {@link BufferedImage} into the right type.
 * 
 * </p>
 */

class MediaWriter extends AMediaCoderMixin
implements IMediaWriter
{
  final private Logger log = LoggerFactory.getLogger(this.getClass());
  { log.trace("<init>"); }

  static
  {
    com.xuggle.ferry.JNIMemoryManager.setMemoryModel(
      com.xuggle.ferry.JNIMemoryManager.MemoryModel.NATIVE_BUFFERS);
  }


  /** The default pixel type. */

  private static final IPixelFormat.Type DEFAULT_PIXEL_TYPE = 
    IPixelFormat.Type.YUV420P;

  /** The default sample format. */

  private static final IAudioSamples.Format DEFAULT_SAMPLE_FORMAT = 
    IAudioSamples.Format.FMT_S16;

  /** The default time base. */

  private static final IRational DEFAULT_TIMEBASE = IRational.make(
    1, (int)Global.DEFAULT_PTS_PER_SECOND);

  // the input container of packets
  
  private final IContainer mInputContainer;

  // the container format

  private IContainerFormat mContainerFormat;

  // a map between input stream indicies to output stream indicies

  private Map<Integer, Integer> mOutputStreamIndices = 
    new HashMap<Integer, Integer>();

  // a map between output stream indicies and streams

  private Map<Integer, IStream> mStreams = 
    new HashMap<Integer, IStream>();

  // a map between output stream indicies and video converters

  private Map<Integer, IConverter> mVideoConverters = 
    new HashMap<Integer, IConverter>();
  
  // streasm opened by this MediaWriter must be closed

  private final Collection<IStream> mOpenedStreams = new Vector<IStream>();

  // true if the writer should ask FFMPEG to interleave media

  private boolean mForceInterleave = true;

  // mask late stream exception policy
  
  private boolean mMaskLateStreamException = false;

  /**
   * Use a specified {@link IMediaReader} as a source for media data and
   * meta data about the container and it's streams.  The {@link
   * IMediaReader} must be configured such that streams will not be
   * dynamically added to the container, which is the default for {@link
   * IMediaReader}.
   * 
   * @param url the url or filename of the media destination
   * @param reader the media source
   * 
   * @throws IllegalArgumentException if the specifed {@link
   *         IMediaReader} is configure to allow dynamic adding of
   *         streams.
   */

  MediaWriter(String url, IMediaReader reader)
  {
    // construct around the source container

    this(url, reader.getContainer());

    // if the container can add streams dynamically, it is not
    // currently supported, throw an exception.  this kind of test needs
    // to be done both here and in the constructor which takes a
    // container because the MediaReader may not have opened it's
    // internal container and thus not set this flag yet

    if (reader.canAddDynamicStreams())
      throw new IllegalArgumentException(
        "inputContainer is improperly configured to allow " + 
        "dynamic adding of streams.");
  }

  /**
   * Use a specified {@link IContainer} as a source for and meta data
   * about the container and it's streams.  The {@link IContainer} must
   * be configured such that streams will not be dynamically added to the
   * container.
   * 
   * @param url the url or filename of the media destination
   * @param inputContainer the source media container
   * 
   * @throws IllegalArgumentException if the specifed {@link IContainer}
   *         is not a of type READ or is configure to allow dynamic
   *         adding of streams.
   */

  MediaWriter(String url, IContainer inputContainer)
  {
    super(url, IContainer.make());

    // verify that the input container is a readable type

    if (inputContainer.getType() != IContainer.Type.READ)
      throw new IllegalArgumentException(
        "inputContainer is improperly must be of type readable.");

    // verify that no streams will be added dynamically

    if (inputContainer.canStreamsBeAddedDynamically())
      throw new IllegalArgumentException(
        "inputContainer is improperly configured to allow " + 
        "dynamic adding of streams.");

    // record the input container and url

    mInputContainer = inputContainer;

    // create format 

    mContainerFormat = IContainerFormat.make();
    mContainerFormat.setOutputFormat(mInputContainer.getContainerFormat().
      getInputFormatShortName(), getUrl(), null);
  }

  /**
   * Create a MediaWriter which will require subsequent calls to {@link
   * #addVideoStream} and/or {@link #addAudioStream} to configure the
   * writer.  Streams may be added or further configured as needed until
   * the first attempt to write data.
   * 
   * <p>
   *
   * To write data call to {@link #onAudioSamples} and/or {@link
   * #onVideoPicture}.
   *
   * </p>
   *
   * @param url the url or filename of the media destination
   */

  MediaWriter(String url)
  {
    super(url, IContainer.make());

    // record the url and absense of the input container 

    mInputContainer = null;

    // create null container format
    
    mContainerFormat = null;
  }

  public int addAudioStream(int inputIndex, int streamId,
      int channelCount, int sampleRate)
  {
    IContainerFormat format = null;
    if (getContainer() != null)
      format = getContainer().getContainerFormat();
    if (format != null && !format.isOutput())
    {
      format.delete();
      format = null;
    }
    String url = getUrl();
    if (format == null && (url == null || url.length()<0))
      throw new IllegalArgumentException("Cannot guess codec without container or url");
    ICodec codec = ICodec.guessEncodingCodec(format,
        null, url, null,
        ICodec.Type.CODEC_TYPE_AUDIO);
    if (codec == null)
      throw new UnsupportedOperationException("could not guess audio codec");
    
    try {
      return addAudioStream(inputIndex, streamId, codec,
          channelCount, sampleRate);
    }
    finally
    {
      if (codec != null)
        codec.delete();
    }
  }
  
  public int addAudioStream(int inputIndex, int streamId,
      ICodec.ID codecId, int channelCount, int sampleRate)
  {
    if (codecId == null)
      throw new IllegalArgumentException("null codecId");
    ICodec codec = ICodec.findEncodingCodec(codecId);
    if (codec == null)
      throw new UnsupportedOperationException("cannot encode with codec: "+
          codecId);
    try
    {
      return addAudioStream(inputIndex, streamId, codec,
          channelCount, sampleRate);
    }
    finally
    {
      codec.delete();
    }
  }

  /** 
   * Add a audio stream.  The time base defaults to {@link
   * #DEFAULT_TIMEBASE} and the audio format defaults to {@link
   * #DEFAULT_SAMPLE_FORMAT}.  The new {@link IStream} is returned to
   * provide an easy way to further configure the stream.
   * 
   * @param inputIndex the index that will be passed to {@link
   *        #onAudioSamples} for this stream
   * @param streamId a format-dependent id for this stream
   * @param codec the codec to used to encode data, to establish the
   *        codec see {@link com.xuggle.xuggler.ICodec}
   * @param channelCount the number of audio channels for the stream
   * @param sampleRate sample rate in Hz (samples per seconds), common
   *        values are 44100, 22050, 11025, etc.
   *
   * @throws IllegalArgumentException if inputIndex < 0, the stream id <
   *         0, the codec is NULL or if the container is already open.
   * @throws IllegalArgumentException if width or height are <= 0
   * 
   * @see IContainer
   * @see IStream
   * @see IStreamCoder
   * @see ICodec
   */

  public int addAudioStream(int inputIndex, int streamId, ICodec codec,
    int channelCount, int sampleRate)
  {
    // validate parameteres

    if (channelCount <= 0)
      throw new IllegalArgumentException(
        "invalid channel count " + channelCount);
    if (sampleRate <= 0)
      throw new IllegalArgumentException(
        "invalid sample rate " + sampleRate);

    // add the new stream at the correct index

    IStream stream = establishStream(inputIndex, streamId, codec);
    
    // configre the stream coder

    IStreamCoder coder = stream.getStreamCoder();
    coder.setChannels(channelCount);
    coder.setSampleRate(sampleRate);
    coder.setSampleFormat(DEFAULT_SAMPLE_FORMAT);

    // add the stream to the media writer
    
    addStream(stream, inputIndex, stream.getIndex());

    // return the new audio stream

    return stream.getIndex();
  }

  
  public int addVideoStream(int inputIndex, int streamId,
      int width, int height)
  {
    return addVideoStream(inputIndex, streamId, 
        (IRational)null, width,height);
  }
  
  public int addVideoStream(int inputIndex, int streamId,
      IRational frameRate,
      int width, int height)
  {
    IContainerFormat format = null;
    if (getContainer() != null)
      format = getContainer().getContainerFormat();
    if (format != null && !format.isOutput())
    {
      format.delete();
      format = null;
    }
    String url = getUrl();
    if (format == null && (url == null || url.length()<0))
      throw new IllegalArgumentException("Cannot guess codec without container or url");
    ICodec codec = ICodec.guessEncodingCodec(format,
        null, url, null,
        ICodec.Type.CODEC_TYPE_VIDEO);
    if (codec == null)
      throw new UnsupportedOperationException("could not guess video codec");
    
    try {
      return addVideoStream(inputIndex, streamId,
          codec, frameRate,
          width, height);
    }
    finally
    {
      if (codec != null)
        codec.delete();
    }    
  }
  
  public int addVideoStream(int inputIndex, int streamId,
      ICodec.ID codecId, int width, int height)
  {
    return addVideoStream(inputIndex, streamId, codecId,
        null, width, height);
  }
  public int addVideoStream(int inputIndex, int streamId,
      ICodec.ID codecId, IRational frameRate, int width, int height)
  {
    if (codecId == null)
      throw new IllegalArgumentException("null codecId");
    ICodec codec = ICodec.findEncodingCodec(codecId);
    if (codec == null)
      throw new UnsupportedOperationException("cannot encode with codec: "+
          codecId);
    try
    {
      return addVideoStream(inputIndex, streamId, codec, 
          frameRate, width, height);
    }
    finally
    {
      codec.delete();
    }
  }
  
  public int addVideoStream(int inputIndex, int streamId,
      ICodec codec, 
      int width, int height)
  {
    return addVideoStream(inputIndex, streamId, codec,
        null, width, height);
  }
  /** 
   * Add a video stream.  The time base defaults to {@link
   * #DEFAULT_TIMEBASE} and the pixel format defaults to {@link
   * #DEFAULT_PIXEL_TYPE}.  The new {@link IStream} is returned to
   * provide an easy way to further configure the stream.
   * 
   * @param inputIndex the index that will be passed to {@link
   *        #onVideoPicture} for this stream
   * @param streamId a format-dependent id for this stream
   * @param codec the codec to used to encode data, to establish the
   *        codec see {@link com.xuggle.xuggler.ICodec}
   * @param width width of video frames
   * @param height height of video frames
   *
   * @throws IllegalArgumentException if inputIndex < 0, the stream id <
   *         0, the codec is NULL or if the container is already open.
   * @throws IllegalArgumentException if width or height are <= 0
   * 
   * @see IContainer
   * @see IStream
   * @see IStreamCoder
   * @see ICodec
   */

  public int addVideoStream(int inputIndex, int streamId,
      ICodec codec, IRational frameRate,
      int width, int height)
  {
    // validate parameteres

    if (width <= 0 || height <= 0)
      throw new IllegalArgumentException(
        "invalid video frame size [" + width + " x " + height + "]");

    // add the new stream at the correct index

    IStream stream = establishStream(inputIndex, streamId, codec);
    
    // configre the stream coder

    IStreamCoder coder = stream.getStreamCoder();
    try
    {
      List<IRational> supportedFrameRates = codec.getSupportedVideoFrameRates();
      IRational timeBase = null;
      if (supportedFrameRates != null && supportedFrameRates.size() > 0)
      {
        IRational highestResolution = null;
        // If we have a list of supported frame rates, then
        // we must pick at least one of them.  and if the
        // user passed in a frameRate, it must match 
        // this list.
        for(IRational supportedRate: supportedFrameRates)
        {
          if (!IRational.positive(supportedRate))
            continue;
          if (highestResolution == null)
            highestResolution = supportedRate.copyReference();

          if (IRational.positive(frameRate))
          {
            if (supportedRate.compareTo(frameRate) == 0)
              // use this
              highestResolution = frameRate.copyReference();
          }
          else if (highestResolution.getDouble() < supportedRate.getDouble())
          {
            highestResolution.delete();
            highestResolution = supportedRate.copyReference();
          }
          supportedRate.delete();
        }
        // if we had a frame rate suggested, but we
        // didn't find a match among the supported elements,
        // throw an error.
        if (IRational.positive(frameRate) &&
            (highestResolution == null ||
                highestResolution.compareTo(frameRate) != 0))
          throw new UnsupportedOperationException("container does not"+
              " support encoding at given frame rate: " + frameRate);
        
        // if we got through the supported list and found NO valid
        // resolution, fail.
        if (highestResolution == null)
          throw new UnsupportedOperationException(
              "could not find supported frame rate for container: " +
              getUrl());
        if (timeBase == null)
          timeBase = IRational.make(highestResolution.getDenominator(),
              highestResolution.getNumerator());
        highestResolution.delete();
        highestResolution = null;
      }
      // if a positive frame rate was passed in, we
      // should either use the inverse of it, or if
      // there is a supported frame rate, but not
      // this, then throw an error.
      if (IRational.positive(frameRate) && timeBase == null)
      {
        timeBase = IRational.make(
            frameRate.getDenominator(),
            frameRate.getNumerator());
      }
      
      if (timeBase == null)
      {
        timeBase = getDefaultTimebase();
        
        // Finally MPEG4 has some code failing if the time base
        // is too aggressive...
        if (codec.getID() == ICodec.ID.CODEC_ID_MPEG4 &&
            timeBase.getDenominator() > ((1<<16)-1))
        {
          // this codec can't support that high of a frame rate
          timeBase.delete();
          timeBase = IRational.make(1,(1<<16)-1);
        }
      }
      coder.setTimeBase(timeBase);
      timeBase.delete();
      timeBase= null;

      coder.setWidth(width);
      coder.setHeight(height);
      coder.setPixelType(DEFAULT_PIXEL_TYPE);

      // add the stream to the media writer

      addStream(stream, inputIndex, stream.getIndex());
    }
    finally
    {
      coder.delete();
    }

    // return the new video stream

    return stream.getIndex();
  }

  /** 
   * Add a generic stream the this writer.  This method is intended for
   * internal use.
   * 
   * @param inputIndex the index that will be passed to {@link
   *        #onVideoPicture} for this stream
   * @param streamId a format-dependent id for this stream
   * @param codec the codec to used to encode data
   *
   * @throws IllegalArgumentException if inputIndex < 0, the stream id <
   *         0, the codec is NULL or if the container is already open.
   */

  private IStream establishStream(int inputIndex, int streamId, ICodec codec)
  {
    // validate parameteres and conditions

    if (inputIndex < 0)
      throw new IllegalArgumentException("invalid input index " + inputIndex);
    if (streamId < 0)
      throw new IllegalArgumentException("invalid stream id " + streamId);
    if (null == codec)
      throw new IllegalArgumentException("null codec");

    // if the container is not opened, do so

    if (!isOpen())
      open();

    // add the new stream at the correct index

    IStream stream = getContainer().addNewStream(codec);
    if (stream == null)
      throw new RuntimeException("Unable to create stream id " + streamId +
        ", index " + inputIndex + ", codec " + codec);
    
    // if the stream count is 1, don't force interleave

    setForceInterleave(getContainer().getNumStreams() != 1);

    // return the new video stream

    return stream;
  }


  /**
   * Set late stream exception policy.  When onVideoPicture or
   * onAudioSamples is passed an unrecognized stream index after the the
   * header has been written, either an exception is raised, or the
   * media data is silently ignored.  By default exceptions are raised,
   * not masked.
   *
   * @param maskLateStreamExceptions true if late med
   * 
   * @see #willMaskLateStreamExceptions
   */

  public void setMaskLateStreamExceptions(boolean maskLateStreamExceptions)
  {
    mMaskLateStreamException = maskLateStreamExceptions;
  }
  
  /** 
   * Get the late stream exception policy.  When onVideoPicture or
   * onAudioSamples is passed an unrecognized stream index after the the
   * header has been written, either an exception is raised, or the
   * media data is silently ignored.  By default exceptions are raised,
   * not masked.
   *
   * @return true if late stream data raises exceptions
   * 
   * @see #setMaskLateStreamExceptions
   */

  public boolean willMaskLateStreamExceptions()
  {
    return mMaskLateStreamException;
  }

  /**
   * Set the force interleave option.
   *
   * <p>
   * 
   * If false the media data will be left in the order in which it is
   * presented to the MediaWriter.
   * 
   * </p>
   * <p>
   *
   * If true MediaWriter will ask Xuggler to place media data in time
   * stamp order, which is required for streaming media.
   *
   * <p>
   *
   * @param forceInterleave true if the MediaWriter should force
   *        interleaving of media data
   *
   * @see #willForceInterleave
   */

  public void setForceInterleave(boolean forceInterleave)
  {
    mForceInterleave = forceInterleave;
  }

  /**
   * Test if the MediaWriter will forcibly interleave media data.
   * The default value for this value is true.
   *
   * @return true if MediaWriter forces Xuggler to interleave media data.
   *
   * @see #setForceInterleave
   */

  public boolean willForceInterleave()
  {
    return mForceInterleave;
  }

  /** 
   * Map an input stream index to an output stream index.
   *
   * @param inputStreamIndex the input stream index value
   *
   * @return the associated output stream index or null, if the input
   *         stream index has not been mapped to an output index.
   */

  public Integer getOutputStreamIndex(int inputStreamIndex)
  {
    return mOutputStreamIndices.get(inputStreamIndex);
  }

  private void encodeVideo(int streamIndex, IVideoPicture picture,
      BufferedImage image)
  {
    // establish the stream, return silently if no stream returned
    if (null == picture)
      throw new IllegalArgumentException("no picture");
    
    IStream stream = getStream(streamIndex);
    if (null == stream)
      return;

    // verify parameters

    Integer outputIndex = getOutputStreamIndex(streamIndex);
    if (null == outputIndex)
      throw new IllegalArgumentException("unknow stream index: " + streamIndex);
    if (CODEC_TYPE_VIDEO  != mStreams.get(outputIndex).getStreamCoder()
      .getCodecType())
    {
      throw new IllegalArgumentException("stream[" + streamIndex + 
        "] is not video");
    }
    // encode video picture

    // encode the video packet
    
    IPacket packet = IPacket.make();
    try {
      if (stream.getStreamCoder().encodeVideo(packet, picture, 0) < 0)
        throw new RuntimeException("failed to encode video");
  
      if (packet.isComplete())
        writePacket(packet);
    } finally {
      if (packet != null)
        packet.delete();
    }
  
    // inform listeners

    super.onVideoPicture(new VideoPictureEvent(this, picture, image,
        picture.getTimeStamp(), TimeUnit.MICROSECONDS, streamIndex));

  }

  
  public void encodeVideo(int streamIndex, IVideoPicture picture)
  {
    encodeVideo(streamIndex, picture, null);
  }

  
  public void encodeVideo(int streamIndex, BufferedImage image, long timeStamp, 
    TimeUnit timeUnit)
  {
    // verify parameters

    if (null == image)
      throw new IllegalArgumentException("NULL input image");
    if (null == timeUnit)
      throw new IllegalArgumentException("NULL time unit");

    // try to set up the stream, and if we're not going to encode
    // it, don't bother converting it.
    IStream stream = getStream(streamIndex);
    if (null == stream)
      return;

    // convert the image to a picture and push it off to be encoded

    IVideoPicture picture = convertToPicture(streamIndex, 
      image, MICROSECONDS.convert(timeStamp, timeUnit));

    try
    {
      encodeVideo(streamIndex, picture, image);
    } 
    finally 
    {
      if (picture != null)
        picture.delete();
    }
  }


  /** {@inheritDoc} */
  
  
  public void encodeAudio(
      int streamIndex, IAudioSamples samples)
  {
    if (null == samples)
      throw new IllegalArgumentException("NULL input samples");
    // establish the stream, return silently if no stream returned

    IStream stream = getStream(streamIndex);
    if (null == stream)
      return;

    IStreamCoder coder = stream.getStreamCoder();
    try
    {
      if (CODEC_TYPE_AUDIO != coder.getCodecType())
      {
        throw new IllegalArgumentException("stream[" + streamIndex + 
        "] is not audio");
      }

      // encode the audio

      // convert the samples into a packet

      for (int consumed = 0; consumed < samples.getNumSamples(); /* in loop */)
      {
        // encode audio

        IPacket packet = IPacket.make();
        try {
          int result = coder.encodeAudio(packet, samples, consumed); 
          if (result < 0)
            throw new RuntimeException("failed to encode audio");

          // update total consumed

          consumed += result;

          // if a complete packed was produced write it out

          if (packet.isComplete())
            writePacket(packet);
        } finally {
          if (packet != null)
            packet.delete();
        }
      }      // inform listeners

      super.onAudioSamples(new AudioSamplesEvent(this, samples,
          streamIndex));
    }
    finally
    {
      if (coder != null) coder.delete();
    }
  }

  
  public void encodeAudio(int streamIndex, short[] samples, 
    long timeStamp, TimeUnit timeUnit)
  {
    // verify parameters
    if (null == samples)
      throw new IllegalArgumentException("NULL input samples");

    IStream stream = getStream(streamIndex);
    if (null == stream)
      return;

    IStreamCoder coder = stream.getStreamCoder();
    try
    {
      if (IAudioSamples.Format.FMT_S16 != coder.getSampleFormat())
      {
        throw new IllegalArgumentException("stream[" + streamIndex
            + "] is not 16 bit audio");
      }

      // establish the number of samples

      long sampleCount = samples.length / coder.getChannels();

      // create the audio samples object and extract the internal buffer
      // as an array

      IAudioSamples audioFrame = IAudioSamples.make(sampleCount, coder
          .getChannels());

      /**
       * We allow people to pass in a null timeUnit for audio as
       * a signal that time stamps are unknown.  This is a common
       * case for audio data, and Xuggler should handle it if
       * we set a invalid time stamp on the audio.
       */
      final long timeStampMicro;
      if (timeUnit == null)
        timeStampMicro = Global.NO_PTS;
      else
        timeStampMicro = MICROSECONDS.convert(timeStamp, timeUnit);

      audioFrame.setComplete(true, sampleCount, coder.getSampleRate(), coder
          .getChannels(), coder.getSampleFormat(), timeStampMicro);

      audioFrame.put(samples, 0, 0, samples.length);
      encodeAudio(streamIndex, audioFrame);
    }
    finally
    {
      if (coder != null)
        coder.delete();
    }
  }

  public void encodeAudio(int streamIndex, short[] samples)
  {
    encodeAudio(streamIndex, samples, Global.NO_PTS, null);
  }
  
  /** 
   * Convert an image to a picture for a given stream.
   * 
   * @param stream to destination stream of the image
   */

  private IVideoPicture convertToPicture(int streamIndex, BufferedImage image,
    long timeStamp)
  {
    // lookup the converter

    IConverter videoConverter = mVideoConverters.get(streamIndex);

    // if not found create one

    if (videoConverter == null)
    {
      IStream stream = mStreams.get(streamIndex);
      IStreamCoder coder = stream.getStreamCoder();
      videoConverter = ConverterFactory.createConverter(
        ConverterFactory.findDescriptor(image),
        coder.getPixelType(),
        coder.getWidth(), coder.getHeight(),
        image.getWidth(), image.getHeight());
      mVideoConverters.put(streamIndex, videoConverter);
    }

    // return the converter
    
    return videoConverter.toPicture(image, timeStamp);
  }
  
  /** 
   * Get the correct {@link IStream} for a given stream index in the
   * container.  If this has been seen before, it
   * is assumed to be a new stream and construct the correct coder for
   * it.
   *
   * @param inputStreamIndex the input index of the stream for which to
   *        find the coder
   * 
   * @return the coder which will be used to encode data for the
   *         specified stream
   */

  private IStream getStream(int inputStreamIndex)
  {
    // the output container must be open

    if (!isOpen())
      open();
    
    // if the output stream index does not exists, create it

    if (null == getOutputStreamIndex(inputStreamIndex))
    {
      // If the header has already been written, then it is too late to
      // establish a new stream, throw, or mask optionally mask, and
      // exception regarding the tardy arrival of the new stream

      if (getContainer().isHeaderWritten())
        if (willMaskLateStreamExceptions())
          return null;
        else
          throw new RuntimeException("Input stream index " + inputStreamIndex + 
            " has not been seen before, but the media header has already been " +
            "written.  To mask these exceptions call setMaskLateStreamExceptions()");

      // if an no input container exists, create new a stream from scratch

      if (null == mInputContainer)
      {
        //
        // NOTE: this is where the new stream code will go
        //

        throw new UnsupportedOperationException(
          "MediaWriter can not yet create streams without an input container.");
      }

      // otherwise use the input container as a guide to adding streams
      
      else
      {
        // the input container must be open

        if (!mInputContainer.isOpened())
          throw new RuntimeException(
            "Can't get stream information from a closed input IContainer.");

        // have a look through the input container streams

        for (int i = 0; i < mInputContainer.getNumStreams(); ++i)
        {
          // if input stream index does not map to an output stream
          // index, this is a new stream, add it

          if (null == mOutputStreamIndices.get(i))
            addStreamFromContainer(i);
        }
      }
    }

    // if the header has not been written, do so now
    
    if (!getContainer().isHeaderWritten())
    {
      // if any of the existing coders are not open, open them now

      for (IStream stream: mStreams.values())
        if (!stream.getStreamCoder().isOpen())
          openStream(stream);

      // write the header

      int rv = getContainer().writeHeader();
      if (0 != rv)
        throw new RuntimeException("Error " + IError.make(rv) +
          ", failed to write header to container " + getContainer() +
          " while establishing stream " + 
          mStreams.get(getOutputStreamIndex(inputStreamIndex)));

      // inform the listeners

      super.onWriteHeader(new WriteHeaderEvent(this));
    }
    
    // establish the coder for the output stream index

    IStream stream = mStreams.get(getOutputStreamIndex(inputStreamIndex));
    if (null == stream)
      throw new RuntimeException("invalid input stream index (no stream): "
         + inputStreamIndex);
    IStreamCoder coder = stream.getStreamCoder();
    if (null == coder)
      throw new RuntimeException("invalid input stream index (no coder): "
        + inputStreamIndex);
    
    // return the coder
    
    return stream;
  }

  /**
   * Test if the {@link MediaWriter} can write streams
   * of this {@link ICodec.Type}
   * 
   * @param type the type of codec to be tested
   *
   * @return true if codec type is supported type
   */

  public boolean isSupportedCodecType(ICodec.Type type)
  {
    return (CODEC_TYPE_VIDEO == type || CODEC_TYPE_AUDIO == type);
  }

  /**
   * Construct a stream  using the mInputContainer information.
   *
   * @param inputStreamIndex the index of the stream on the input
   *   container
   * 
   * @return true if the stream was added, false if it's not a supported
   *   stream type
   */

  private boolean addStreamFromContainer(int inputStreamIndex)
  {
    // get the input stream

    IStream inputStream = mInputContainer.getStream(inputStreamIndex);
    IStreamCoder inputCoder = inputStream.getStreamCoder();
    ICodec.Type inputType = inputCoder.getCodecType();
    ICodec.ID inputID = inputCoder.getCodecID();
    
    // if this stream is not a supported type, indicate failure

    if (!isSupportedCodecType(inputType))
      return false;

    IContainerFormat format = getContainer().getContainerFormat();
    
    switch(inputType)
    {
      case CODEC_TYPE_AUDIO:
        addAudioStream(inputStream.getIndex(),
            inputStream.getId(),
            format.establishOutputCodecId(inputID),
            inputCoder.getChannels(),
            inputCoder.getSampleRate());
        break;
      case CODEC_TYPE_VIDEO:
        addVideoStream(inputStream.getIndex(),
            inputStream.getId(),
            format.establishOutputCodecId(inputID),
            inputCoder.getFrameRate(),
            inputCoder.getWidth(),
            inputCoder.getHeight());
        break;
      default:
        break;
    }
    return true;
  }

  /**
   * Add a stream.
   */
  
  private void addStream(IStream stream, int inputStreamIndex, 
    int outputStreamIndex)
  {
    // map input to output stream indicies
    
    mOutputStreamIndices.put(inputStreamIndex, outputStreamIndex);

    // get the coder and add it to the index to coder map

    mStreams.put(outputStreamIndex, stream);

    // if this is a video coder, set the quality

    IStreamCoder coder = stream.getStreamCoder();
    if (CODEC_TYPE_VIDEO == coder.getCodecType())
      coder.setFlag(IStreamCoder.Flags.FLAG_QSCALE, true);
    
    // inform listeners

    super.onAddStream(new AddStreamEvent(this, outputStreamIndex));
  }
  
  /**
   * Open a newly added stream.
   */

  private void openStream(IStream stream)
  {
    // if the coder is not open, open it NOTE: MediaWriter currently
    // supports audio & video streams
    
    IStreamCoder coder = stream.getStreamCoder();
    try
    {
      ICodec.Type type = coder.getCodecType();
      if (!coder.isOpen() && isSupportedCodecType(type))
      {
        // open the coder

        int rv = coder.open(null, null);
        if (rv < 0)
          throw new RuntimeException("could not open stream " + stream + ": "
              + getErrorMessage(rv));
        mOpenedStreams.add(stream);

        // inform listeners
        super.onOpenCoder(new OpenCoderEvent(this, stream.getIndex()));
      }
    }
    finally
    {
      coder.delete();
    }
  }
  
  /**
   * Write packet to the output container
   * 
   * @param packet the packet to write out
   */

  private void writePacket(IPacket packet)
  {
    if (getContainer().writePacket(packet, mForceInterleave)<0)
      throw new RuntimeException("failed to write packet: " + packet);

    // inform listeners

    super.onWritePacket(new WritePacketEvent(this,packet));
  }

  /** 
   * Flush any remaining media data in the media coders.
   */

  public void flush()
  {
    // flush coders

    for (IStream stream: mStreams.values())
    {
      IStreamCoder coder = stream.getStreamCoder();
      if (!coder.isOpen())
        continue;

      // if it's audio coder flush that

      if (CODEC_TYPE_AUDIO == coder.getCodecType())
      {
        IPacket packet = IPacket.make();
        while (coder.encodeAudio(packet, null, 0) >= 0 && packet.isComplete())
        {
          writePacket(packet);
          packet.delete();
          packet = IPacket.make();
        }
        packet.delete();
      }
      
      // else flush video coder

      else if (CODEC_TYPE_VIDEO == coder.getCodecType())
      {
        IPacket packet = IPacket.make();
        while (coder.encodeVideo(packet, null, 0) >= 0 && packet.isComplete())
        {
          writePacket(packet);
          packet.delete();
          packet = IPacket.make();
        }
        packet.delete();
      }
    }

    // flush the container

    getContainer().flushPackets();

    // inform listeners

    super.onFlush(new FlushEvent(this));
  }

  /** {@inheritDoc} */

  public void open()
  {
    // open the container

    if (getContainer().open(getUrl(), IContainer.Type.WRITE, mContainerFormat,
        true, false) < 0)
      throw new IllegalArgumentException("could not open: " + getUrl());

    // inform listeners

    super.onOpen(new OpenEvent(this));
    
    // note that we should close the container opened here

    setShouldCloseContainer(true);
  }

  /** {@inheritDoc} */
  
  public void close()
  {
    int rv;

    // flush coders
    
    flush();

    // write the trailer on the output conteiner
    
    if ((rv = getContainer().writeTrailer()) < 0)
      throw new RuntimeException("error " + IError.make(rv) +
        ", failed to write trailer to "
        + getUrl());

    // inform the listeners

    super.onWriteTrailer(new WriteTrailerEvent(this));
    
    // close the coders opened by this MediaWriter

    for (IStream stream: mOpenedStreams)
    {
      IStreamCoder coder = stream.getStreamCoder();
      try
      {
        if ((rv = coder.close()) < 0)
          throw new RuntimeException("error "
              + getErrorMessage(rv)
              + ", failed close coder " + coder);

        // inform the listeners
        super.onCloseCoder(new CloseCoderEvent(this, stream.getIndex()));
      }
      finally
      {
        coder.delete();
      }
    }

    // expunge all referneces to the coders and resamplers
    
    mStreams.clear();
    mOpenedStreams.clear();
    mVideoConverters.clear();

    // if we're supposed to, close the container

    if (getShouldCloseContainer())
    {
      if ((rv = getContainer().close()) < 0)
        throw new RuntimeException("error " + IError.make(rv) +
          ", failed close IContainer " +
          getContainer() + " for " + getUrl());
      setShouldCloseContainer(false);
    }

    // inform the listeners

    super.onClose(new CloseEvent(this));
  }

  /**
   * Get the default pixel type
   * @return the default pixel type
   */
  public IPixelFormat.Type getDefaultPixelType()
  {
    return DEFAULT_PIXEL_TYPE;
  }

  /**
   * Get the default audio sample format
   * @return the format
   */
  public IAudioSamples.Format getDefaultSampleFormat()
  {
    return DEFAULT_SAMPLE_FORMAT;
  }

  /**
   * Get the default time base we'll use on our encoders
   * if one is not specified by the codec.
   * @return the default time base
   */
  public IRational getDefaultTimebase()
  {
    return DEFAULT_TIMEBASE.copyReference();
  }

  /** {@inheritDoc} */

  public String toString()
  {
    return "MediaWriter[" + getUrl() + "]";
  }

  /** {@inheritDoc} */

  public void onOpen(IOpenEvent event)
  {
  }

  /** {@inheritDoc} */

  public void onClose(ICloseEvent event)
  {
    if (isOpen())
      close();
  }

  /** {@inheritDoc} */

  public void onAddStream(IAddStreamEvent event)
  {
  }

  /** {@inheritDoc} */

  public void onOpenCoder(IOpenCoderEvent event)
  {
  }

  /** {@inheritDoc} */

  public void onCloseCoder(ICloseCoderEvent event)
  {
  }

  /** {@inheritDoc} */

  public void onVideoPicture(IVideoPictureEvent event)
  {
    if (event.getImage() != null)
      encodeVideo(event.getStreamIndex(),
          event.getImage(),
          event.getTimeStamp(event.getTimeUnit()),
          event.getTimeUnit());
    else
      encodeVideo(event.getStreamIndex(), event.getPicture());
  }

  /** {@inheritDoc} */

  public void onAudioSamples(IAudioSamplesEvent event)
  {
    encodeAudio(event.getStreamIndex(), event.getAudioSamples());
  }

  /** {@inheritDoc} */

  public void onReadPacket(IReadPacketEvent event)
  {
  }

  /** {@inheritDoc} */

  public void onWritePacket(IWritePacketEvent event)
  {
  }

  /** {@inheritDoc} */

  public void onWriteHeader(IWriteHeaderEvent event)
  {
  }

  /** {@inheritDoc} */

  public void onFlush(IFlushEvent event)
  {
  }

  /** {@inheritDoc} */

  public void onWriteTrailer(IWriteTrailerEvent event)
  {
  }
  
  private static String getErrorMessage(int rv)
  {
    String errorString = "";
    IError error = IError.make(rv);
    if (error != null) {
       errorString = error.toString();
       error.delete();
    }
    return errorString;
  }


}
