"use client";

import React, { useEffect, useState, useCallback } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import AdDisplay from '@/components/AdDisplay';

interface Listing {
    id: number;
    title: string;
    description: string;
    price: string;
    property_type: string;
    bedrooms: string;
    bathrooms: string;
    square_footage?: string;
    address: string;
    city: string;
    province: string;
    postal_code?: string;
    main_image_url?: string;
    image_urls?: string[];
    amenities?: string[];
    contact_email: string;
    contact_phone?: string;
    status?: string;
    listing_tier?: string;
    created_at?: string;
    updated_at?: string;
    user_id?: number; // Assuming we might want to show agent info later
}

async function fetchListingDetail(listingId: string): Promise<Listing | null> {
    try {
        // No token needed for public listing view, assuming backend endpoint is public
        const response = await fetch(`http://localhost:5000/api/listings/listings/${listingId}`); 
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || `Failed to fetch listing ${listingId}`);
        }
        const data = await response.json();
        return data.listing; // Assuming the API returns { listing: Listing }
    } catch (error) {
        console.error("Error fetching listing detail:", error);
        throw error;
    }
}

export default function ListingDetailPage() {
    const router = useRouter();
    const params = useParams();
    const listingId = params?.id as string;

    const [listing, setListing] = useState<Listing | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [currentImageIndex, setCurrentImageIndex] = useState(0);

    const loadListing = useCallback(async () => {
        if (!listingId) {
            setError("Listing ID is missing.");
            setLoading(false);
            return;
        }
        setLoading(true);
        setError(null);
        try {
            const data = await fetchListingDetail(listingId);
            if (!data) {
                setError("Listing not found.");
            } else {
                setListing(data);
            }
        } catch (err: any) {
            setError(err.message || "Could not load listing details.");
        }
        setLoading(false);
    }, [listingId]);

    useEffect(() => {
        loadListing();
    }, [loadListing]);

    const allImages = listing?.main_image_url ? [listing.main_image_url, ...(listing.image_urls || [])] : (listing?.image_urls || []);

    const nextImage = () => {
        if (allImages.length > 0) {
            setCurrentImageIndex((prevIndex) => (prevIndex + 1) % allImages.length);
        }
    };

    const prevImage = () => {
        if (allImages.length > 0) {
            setCurrentImageIndex((prevIndex) => (prevIndex - 1 + allImages.length) % allImages.length);
        }
    };

    if (loading) return <div className="min-h-screen bg-ps-secondary flex justify-center items-center"><p className="text-xl text-ps-primary">Loading listing details...</p></div>;
    if (error) return <div className="min-h-screen bg-ps-secondary flex justify-center items-center"><p className="text-xl text-red-500">Error: {error}</p></div>;
    if (!listing) return <div className="min-h-screen bg-ps-secondary flex justify-center items-center"><p className="text-xl text-ps-text-muted">Listing not found.</p></div>;

    return (
        <div className="min-h-screen bg-ps-secondary font-sans text-ps-text-default">
            <header className="bg-ps-primary text-white p-4 shadow-md">
                <div className="container mx-auto flex justify-between items-center">
                    <Link href="/" legacyBehavior><a className="text-2xl font-serif font-bold">PropertySunday</a></Link>
                    <nav className="space-x-4">
                        <Link href="/listings" legacyBehavior><a className="hover:text-ps-accent">All Listings</a></Link>
                        <Link href="/account/my-listings" legacyBehavior><a className="hover:text-ps-accent">My Listings</a></Link>
                        {/* Add Login/Register or User Profile/Logout based on auth state */}
                    </nav>
                </div>
            </header>

            <main className="container mx-auto p-4 md:p-8 mt-8">
                <div className="bg-white rounded-xl shadow-2xl overflow-hidden border border-ps-neutral-light">
                    {/* Image Gallery Section */}
                    {allImages.length > 0 ? (
                        <div className="relative">
                            <img 
                                src={allImages[currentImageIndex]} 
                                alt={`${listing.title} - Image ${currentImageIndex + 1}`}
                                className="w-full h-[300px] md:h-[500px] object-cover"
                            />
                            {allImages.length > 1 && (
                                <>
                                    <button onClick={prevImage} className="absolute left-4 top-1/2 -translate-y-1/2 bg-black bg-opacity-50 text-white p-3 rounded-full hover:bg-opacity-75 transition-opacity">
                                        &#10094;
                                    </button>
                                    <button onClick={nextImage} className="absolute right-4 top-1/2 -translate-y-1/2 bg-black bg-opacity-50 text-white p-3 rounded-full hover:bg-opacity-75 transition-opacity">
                                        &#10095;
                                    </button>
                                    <div className="absolute bottom-4 left-1/2 -translate-x-1/2 bg-black bg-opacity-70 text-white text-xs px-2 py-1 rounded">
                                        {currentImageIndex + 1} / {allImages.length}
                                    </div>
                                </> 
                            )}
                        </div>
                    ) : (
                        <div className="w-full h-[300px] md:h-[500px] bg-ps-neutral-light flex items-center justify-center text-ps-text-muted">
                            No Images Available
                        </div>
                    )}

                    <div className="p-6 md:p-10">
                        <div className="flex flex-col md:flex-row justify-between items-start mb-4">
                            <h1 className="text-3xl md:text-4xl font-serif font-bold text-ps-primary mb-2 md:mb-0">{listing.title}</h1>
                            {listing.listing_tier && listing.listing_tier !== 'basic' && (
                                <span className={`px-3 py-1 rounded-full text-sm font-semibold capitalize 
                                    ${listing.listing_tier === 'premium' ? 'bg-ps-accent text-white' : 'bg-ps-primary-light text-ps-primary'}`}>
                                    {listing.listing_tier} Listing
                                </span>
                            )}
                        </div>
                        <p className="text-3xl md:text-4xl font-bold text-ps-primary-dark mb-4">R {parseFloat(listing.price).toLocaleString('en-ZA')}</p>
                        
                        <div className="text-sm text-ps-text-muted mb-6">
                            <p>{listing.address}, {listing.city}, {listing.province} {listing.postal_code || ''}</p>
                            {listing.created_at && <p className="mt-1">Listed on: {new Date(listing.created_at).toLocaleDateString()}</p>}
                        </div>

                        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4 mb-8 text-center">
                            <div className="bg-ps-secondary p-4 rounded-lg shadow">
                                <p className="text-xs text-ps-text-muted">Type</p>
                                <p className="font-semibold text-ps-primary-dark text-lg">{listing.property_type}</p>
                            </div>
                            <div className="bg-ps-secondary p-4 rounded-lg shadow">
                                <p className="text-xs text-ps-text-muted">Bedrooms</p>
                                <p className="font-semibold text-ps-primary-dark text-lg">{listing.bedrooms}</p>
                            </div>
                            <div className="bg-ps-secondary p-4 rounded-lg shadow">
                                <p className="text-xs text-ps-text-muted">Bathrooms</p>
                                <p className="font-semibold text-ps-primary-dark text-lg">{listing.bathrooms}</p>
                            </div>
                            {listing.square_footage && (
                                <div className="bg-ps-secondary p-4 rounded-lg shadow">
                                    <p className="text-xs text-ps-text-muted">Size (sqm)</p>
                                    <p className="font-semibold text-ps-primary-dark text-lg">{listing.square_footage}</p>
                                </div>
                            )}
                        </div>

                        <h2 className="text-2xl font-serif font-semibold text-ps-primary mt-8 mb-4">Property Description</h2>
                        <p className="text-ps-text-default leading-relaxed whitespace-pre-line mb-8">
                            {listing.description}
                        </p>

                        {listing.amenities && listing.amenities.length > 0 && (
                            <>
                                <h2 className="text-2xl font-serif font-semibold text-ps-primary mt-8 mb-4">Amenities</h2>
                                <ul className="grid grid-cols-2 md:grid-cols-3 gap-x-6 gap-y-2 text-ps-text-default mb-8">
                                    {listing.amenities.map((amenity, index) => (
                                        <li key={index} className="flex items-center">
                                            <svg className="w-4 h-4 mr-2 text-ps-accent flex-shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd"></path></svg>
                                            {amenity}
                                        </li>
                                    ))}
                                </ul>
                            </>
                        )}

                        <div className="mt-10 pt-8 border-t border-ps-neutral-light">
                            <h2 className="text-2xl font-serif font-semibold text-ps-primary mb-4">Contact Information</h2>
                            <p className="text-ps-text-default">Email: <a href={`mailto:${listing.contact_email}`} className="text-ps-accent hover:underline">{listing.contact_email}</a></p>
                            {listing.contact_phone && <p className="text-ps-text-default">Phone: {listing.contact_phone}</p>}
                            {/* Placeholder for a contact form or agent details */}
                        </div>
                    </div>
                </div>

                {/* Ad Display Section */}
                <div className="mt-12 grid grid-cols-1 md:grid-cols-12 gap-8">
                    <div className="md:col-span-8">
                        {/* Could be related listings or more content */}
                    </div>
                    <aside className="md:col-span-4 space-y-6">
                        <h3 className="text-xl font-serif font-semibold text-ps-primary mb-4">Sponsored</h3>
                        <AdDisplay placementArea="listing_detail_sidebar_top" className="w-full" />
                        <AdDisplay placementArea="listing_detail_sidebar_bottom" className="w-full" />
                    </aside>
                </div>
                <div className="mt-12">
                     <AdDisplay placementArea="listing_detail_footer_banner" className="max-w-full mx-auto" />
                </div>

            </main>

            <footer className="bg-ps-primary-dark text-ps-neutral-light p-8 mt-12 text-center">
                <p>&copy; {new Date().getFullYear()} PropertySunday.com. All rights reserved.</p>
            </footer>
        </div>
    );
}

