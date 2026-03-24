"use client";

import { useState, useEffect, useRef } from "react";
import { Play, Pause, SkipBack, SkipForward, Calendar } from "lucide-react";

interface TimelapseControlProps {
  onDateChange: (date: Date) => void;
  isPlaying: boolean;
  onPlayPause: () => void;
  currentDate: Date;
  startDate: Date;
  endDate: Date;
  speed: number;
  onSpeedChange: (speed: number) => void;
}

export default function TimelapseControl({
  onDateChange,
  isPlaying,
  onPlayPause,
  currentDate,
  startDate,
  endDate,
  speed,
  onSpeedChange,
}: TimelapseControlProps) {
  const [sliderValue, setSliderValue] = useState(0);
  const totalDays = Math.ceil((endDate.getTime() - startDate.getTime()) / (1000 * 60 * 60 * 24));

  useEffect(() => {
    const daysSinceStart = Math.ceil((currentDate.getTime() - startDate.getTime()) / (1000 * 60 * 60 * 24));
    setSliderValue(daysSinceStart);
  }, [currentDate, startDate]);

  const handleSliderChange = (value: number) => {
    setSliderValue(value);
    const newDate = new Date(startDate.getTime() + value * 24 * 60 * 60 * 1000);
    onDateChange(newDate);
  };

  const skipBackward = () => {
    const newValue = Math.max(0, sliderValue - 1);
    handleSliderChange(newValue);
  };

  const skipForward = () => {
    const newValue = Math.min(totalDays, sliderValue + 1);
    handleSliderChange(newValue);
  };

  const formatDate = (date: Date) => {
    return date.toLocaleDateString("th-TH", {
      year: "numeric",
      month: "short",
      day: "numeric",
    });
  };

  return (
    <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 z-[1000] bg-white rounded-lg shadow-2xl p-4 w-[600px]">
      {/* Date Display */}
      <div className="text-center mb-3">
        <div className="flex items-center justify-center gap-2 mb-1">
          <Calendar className="w-4 h-4 text-primary-600" />
          <span className="text-lg font-bold text-primary-900">
            {formatDate(currentDate)}
          </span>
        </div>
        <div className="text-xs text-gray-500">
          {sliderValue} / {totalDays} วัน
        </div>
      </div>

      {/* Timeline Slider */}
      <div className="mb-4">
        <input
          type="range"
          min="0"
          max={totalDays}
          value={sliderValue}
          onChange={(e) => handleSliderChange(parseInt(e.target.value))}
          className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-primary-600"
          style={{
            background: `linear-gradient(to right, #1e40af 0%, #1e40af ${(sliderValue / totalDays) * 100}%, #e5e7eb ${(sliderValue / totalDays) * 100}%, #e5e7eb 100%)`,
          }}
        />
        <div className="flex justify-between text-xs text-gray-500 mt-1">
          <span>{formatDate(startDate)}</span>
          <span>{formatDate(endDate)}</span>
        </div>
      </div>

      {/* Controls */}
      <div className="flex items-center justify-center gap-4">
        {/* Skip Backward */}
        <button
          onClick={skipBackward}
          disabled={sliderValue === 0}
          className="p-2 rounded-full hover:bg-gray-100 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
          title="ย้อนกลับ 1 วัน"
        >
          <SkipBack className="w-5 h-5 text-gray-700" />
        </button>

        {/* Play/Pause */}
        <button
          onClick={onPlayPause}
          className="p-4 rounded-full bg-primary-600 hover:bg-primary-700 text-white transition-colors shadow-lg"
          title={isPlaying ? "หยุด" : "เล่น"}
        >
          {isPlaying ? (
            <Pause className="w-6 h-6" fill="currentColor" />
          ) : (
            <Play className="w-6 h-6" fill="currentColor" />
          )}
        </button>

        {/* Skip Forward */}
        <button
          onClick={skipForward}
          disabled={sliderValue === totalDays}
          className="p-2 rounded-full hover:bg-gray-100 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
          title="ข้ามไป 1 วัน"
        >
          <SkipForward className="w-5 h-5 text-gray-700" />
        </button>
      </div>

      {/* Speed Control */}
      <div className="mt-4 pt-4 border-t">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs font-medium text-gray-600">ความเร็ว</span>
          <span className="text-xs font-bold text-primary-600">{speed}x</span>
        </div>
        <div className="flex gap-2">
          {[0.5, 1, 2, 4].map((s) => (
            <button
              key={s}
              onClick={() => onSpeedChange(s)}
              className={`flex-1 py-1 px-2 text-xs rounded transition-colors ${
                speed === s
                  ? "bg-primary-600 text-white"
                  : "bg-gray-100 text-gray-700 hover:bg-gray-200"
              }`}
            >
              {s}x
            </button>
          ))}
        </div>
      </div>

      {/* Status Indicator */}
      {isPlaying && (
        <div className="mt-3 flex items-center justify-center gap-2 text-xs text-primary-600">
          <div className="w-2 h-2 bg-primary-600 rounded-full animate-pulse"></div>
          <span>กำลังเล่น...</span>
        </div>
      )}
    </div>
  );
}
