"use client";

import React, { useState, useEffect } from 'react';
import Image from 'next/image'; // For optimized images

interface Advertisement {
    id: number;
    title: string;
    advertiser_name: string;
    image_url: string;
    target_url: string;
    placement_area: string;
}

interface AdDisplayProps {
    placementArea: string; // e.g., "homepage_banner", "sidebar_listing"
    className?: string; // Optional additional class names for styling
}

async function fetchAdvertisements(placementArea: string): Promise<Advertisement[]> {
    try {
        // Adjust the API endpoint as per your backend setup
        const response = await fetch(`http://localhost:5000/api/advertisements/advertisements?placement_area=${placementArea}&active_only=true`);
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || `Failed to fetch ads for ${placementArea}`);
        }
        const data = await response.json();
        return data.advertisements || [];
    } catch (error) {
        console.error("Error fetching advertisements:", error);
        return []; // Return empty array on error to prevent breaking the UI
    }
}

async function trackAdImpression(adId: number): Promise<void> {
    try {
        await fetch(`http://localhost:5000/api/advertisements/advertisements/${adId}/track-impression`, { method: 'POST' });
    } catch (error) {
        console.error("Error tracking ad impression:", error);
    }
}

async function trackAdClick(adId: number): Promise<void> {
    try {
        await fetch(`http://localhost:5000/api/advertisements/advertisements/${adId}/track-click`, { method: 'POST' });
    } catch (error) {
        console.error("Error tracking ad click:", error);
    }
}

const AdDisplay: React.FC<AdDisplayProps> = ({ placementArea, className }) => {
    const [ads, setAds] = useState<Advertisement[]>([]);
    const [currentAdIndex, setCurrentAdIndex] = useState(0);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        setIsLoading(true);
        fetchAdvertisements(placementArea)
            .then(fetchedAds => {
                setAds(fetchedAds);
                if (fetchedAds.length > 0) {
                    // Track impression for the first ad shown
                    trackAdImpression(fetchedAds[0].id);
                }
                setIsLoading(false);
            })
            .catch(() => setIsLoading(false)); // Ensure loading is set to false even on error
    }, [placementArea]);

    useEffect(() => {
        if (ads.length <= 1) return; // No need for rotation if 0 or 1 ad

        const intervalId = setInterval(() => {
            setCurrentAdIndex(prevIndex => {
                const nextIndex = (prevIndex + 1) % ads.length;
                // Track impression for the next ad shown in rotation
                trackAdImpression(ads[nextIndex].id);
                return nextIndex;
            });
        }, 7000); // Rotate ads every 7 seconds

        return () => clearInterval(intervalId);
    }, [ads]);

    if (isLoading) {
        return <div className={`p-2 text-center text-sm text-gray-500 ${className}`}>Loading ad...</div>;
    }

    if (ads.length === 0) {
        // Optionally, render a placeholder or nothing if no ads are available
        return null; 
    }

    const currentAd = ads[currentAdIndex];

    const handleAdClick = () => {
        trackAdClick(currentAd.id);
        // Open target_url in a new tab
        window.open(currentAd.target_url, '_blank', 'noopener,noreferrer');
    };

    return (
        <div 
            className={`ad-display-container bg-gray-100 p-2 rounded shadow-md ${className}`}
            onClick={handleAdClick}
            style={{ cursor: 'pointer' }}
            role="button"
            tabIndex={0}
            onKeyPress={(e) => e.key === 'Enter' && handleAdClick()} // Accessibility
            title={`Advertisement: ${currentAd.title} by ${currentAd.advertiser_name}`}
        >
            {currentAd.image_url ? (
                <Image 
                    src={currentAd.image_url} 
                    alt={currentAd.title} 
                    width={300} // Provide appropriate default or dynamic sizes
                    height={250} 
                    className="w-full h-auto object-contain rounded"
                    priority={currentAdIndex === 0} // Prioritize loading the first ad image
                />
            ) : (
                <div className="text-center text-gray-700">
                    <h4 className="font-semibold">{currentAd.title}</h4>
                    <p className="text-sm">by {currentAd.advertiser_name}</p>
                </div>
            )}
            {/* Optional: Display ad title or advertiser name if not part of the image 
            <div className="mt-1 text-xs text-gray-500 text-center">
                {currentAd.title} - Ad by {currentAd.advertiser_name}
            </div>
            */}
        </div>
    );
};

export default AdDisplay;

