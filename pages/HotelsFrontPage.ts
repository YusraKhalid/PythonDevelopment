import {browser} from "protractor";
import HotelsFrontPageElements from "../pageElements/HotelsFrontPageElements";
import {Helper} from "./Helper";

export default class HotelsFrontPage {
    helper = new Helper();
    hotelsFrontPageElementsObj = new HotelsFrontPageElements();
    async goToHotelsFrontPage(): Promise<void> {
        await this.hotelsFrontPageElementsObj.getHotelsBtn().click();
    }
    async isHotelsOriginVisible(): Promise<boolean> {
        const hotelOrigin = this.hotelsFrontPageElementsObj.getHotelsOriginField();
        this.helper.waitForElementToBeVisible(hotelOrigin);
        return hotelOrigin.isDisplayed();
    }
    async isHotelsStartDateVisible(): Promise<boolean> {
        return this.hotelsFrontPageElementsObj.getHotelsStartDateField().isDisplayed();
    }
    async isHotelsEndDateVisible(): Promise<boolean> {
        return this.hotelsFrontPageElementsObj.getHotelsEndDateField().isDisplayed();
    }
    async getGuestFieldText(): Promise<string> {
        return await this.hotelsFrontPageElementsObj.getHotelsGuestField().getAttribute('aria-label');
    }
    async searchByNewHotelsOrigin(): Promise<void> {
        this.hotelsFrontPageElementsObj.getHotelsOriginField().click();
        this.hotelsFrontPageElementsObj.getHotelsOriginInputField().sendKeys('BCN');
        const originDropdown = this.hotelsFrontPageElementsObj.getOriginDropdown();
        this.helper.waitForElementToBeVisible(originDropdown);
        this.hotelsFrontPageElementsObj.getFirstResultOfOriginDropdown().click();
        this.helper.waitForElementToBeInvisible(originDropdown);
        const searchHotelsBtn = this.hotelsFrontPageElementsObj.getSearchHotelsBtn();
        this.helper.waitForElementToBeClickable(searchHotelsBtn);
        searchHotelsBtn.click();
        browser.sleep(20000);
    }
}