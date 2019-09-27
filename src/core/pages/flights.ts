import { MultiCityForm } from "../elements/forms/multiCity";
import { TripSelector } from "../elements/selectors/trip";

export interface FlightsPage {
  getURL(): string;
  
  clickSearch(): Promise<void>;
  
  getTripSelector(): TripSelector;
  
  getMultiCityTripForm(): MultiCityForm;
}
