# Property Portal Integration Research

## PrivateProperty.com

*   **Initial Finding:** Direct API access might require contacting `feeds@privateproperty.co.za`.
*   **User Direction:** Focus on *pulling* listings. Contacting `feeds@privateproperty.co.za` is the primary next step to inquire about a data feed for pulling listings.
*   **Entegral Sync API:** While Entegral lists PrivateProperty.co.za as a supported portal, its primary function appears to be *pushing* listings. Since the user wants to *pull* listings and an Entegral account is not immediate, direct Entegral implementation is paused for PrivateProperty.com integration.

## Property24.com

*   **Initial Finding:** Direct API documentation for Property24.com was not readily found. Unofficial clients are outdated, and some syndication API links were dead.
*   **User Direction:** Focus on *pulling* listings. Scraping is not an option.
*   **Entegral Sync API:** Similar to PrivateProperty.com, Entegral lists Property24.com as a supported portal, but its pull capability is unconfirmed. Direct Entegral implementation is paused for Property24.com integration.
*   **Next Step:** Continue research for any official data feed or API from Property24.com that explicitly supports *pulling* listings. If none are found, this integration will be challenging without a direct partnership or a different syndication service that clearly offers pull functionality.

## General Integration Strategy (Revised based on User Feedback)

*   **Priority:** The core requirement is to *pull* property listings from PrivateProperty.com and Property24.com into PropertySunday.com.
*   **Pushing Listings:** Pushing listings from PropertySunday.com to other portals is not a current priority.
*   **Scraping:** Web scraping is not a desired method.
*   **Syndication (Entegral):** The Entegral Sync API seems primarily for *pushing* listings. Its utility for *pulling* listings is unconfirmed and an account is not immediately available. Therefore, active development with Entegral is on hold pending clarification of its pull capabilities and client readiness for an account.

**Revised Next Steps for Integration:**

1.  **PrivateProperty.com:** Prioritize contacting `feeds@privateproperty.co.za` to inquire about options for a data feed to *pull* listings. (Action: Await user confirmation on drafting/sending this email).
2.  **Property24.com:** Continue dedicated research to find any official mechanism (API, data feed) that allows *pulling* listings from Property24.com.
3.  **Documentation:** If direct pull integrations are not feasible, this will be documented, and the platform will rely on manual listings and any listings users of PropertySunday.com might create themselves.
4.  **Contingency:** The existing manual listing input feature remains the fallback for populating the site.


## Further Research into Property24.com Integration (Syndication Services) - May 12, 2025

Following the difficulty in finding a direct API for *pulling* listings from Property24.com, further investigation into general South African real estate listing syndication services was conducted.

**Key Findings:**

*   Several third-party services offer syndication to major South African property portals, including Property24. Examples found include:
    *   **PropCon:** (https://www.propcon.co.za/real-estate-software/feature/property24-syndication) - This service allows users to load property details once into PropCon's CRM and then *syndicate* (push) those listings to Property24, Private Property, ImmoAfrica, and Gumtree. It also mentions importing analytics and leads *from* Property24 *into* their CRM, but the primary listing flow described is outbound syndication.
    *   **PropData:** (https://www.propdata.net/how-real-estate-listing-syndication-can-work-for-you) - Discusses the benefits of syndication for agents to push listings to multiple portals.
    *   **Cloud Property Solutions:** (https://www.cloudpropertysolutions.com/ListingsSyndicationMoreInfo.html) - States they will "feed your listing information to all the key property portal websites," again implying an outbound (push) mechanism.
    *   **Entegral Sync:** (https://www.entegral.net/sync/) - Previously researched, also focuses on *pushing* listings from a management system to portals.

**Conclusion on Syndication Services for *Pulling* Listings:**

Based on the information available on their websites, these syndication services (PropCon, PropData, Cloud Property Solutions, Entegral) appear to be designed primarily for real estate agencies to *push* their listings from a central management system (like a CRM) *to* various property portals like Property24 and PrivateProperty.

They do not explicitly offer a service or API for a third-party platform (like PropertySunday.com) to *pull* or *ingest* the full range of listings *from* Property24 or PrivateProperty. The "import" features mentioned (e.g., PropCon importing leads/analytics) are typically for the agency's benefit within their CRM, not for providing a data feed of listings to external developers.

Therefore, these syndication platforms, in their described capacity, do not seem to solve the requirement of *pulling* existing listings from Property24.com into PropertySunday.com.

**Next Steps for Integration:**
*   **PrivateProperty.com:** Awaiting user action on contacting `feeds@privateproperty.co.za` (draft email provided) to inquire about a direct data feed for *pulling* listings.
*   **Property24.com:** Direct API or a clear method for *pulling* listings remains elusive. Without an official feed or API supporting this, or a partnership, this integration will be challenging.

This concludes the current phase of research for pulling listings. If direct contact with PrivateProperty.com yields a positive result, that integration can be pursued. For Property24, alternative strategies or direct outreach would be needed if pulling their listings is a firm requirement.
