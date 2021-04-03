import { environment } from '../environments/environment';

let baseUrl: String;
if (environment.production) {
    baseUrl = "https://coactors.ue.r.appspot.com";
}
else {
    baseUrl = "http://127.0.0.1:5000";
}

export {baseUrl};
