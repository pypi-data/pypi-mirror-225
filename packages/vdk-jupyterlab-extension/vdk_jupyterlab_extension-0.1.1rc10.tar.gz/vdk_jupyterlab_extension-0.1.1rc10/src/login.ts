/*
 * Copyright 2021-2023 VMware, Inc.
 * SPDX-License-Identifier: Apache-2.0
 */

import { requestAPI } from './handler';

export async function startLogin() {
  const encodedURL = encodeURIComponent(window.location.href);

  const redirect_url = await requestAPI<any>(
    'login?initial_url=' + encodedURL,
    {
      method: 'GET'
    }
  );
  console.log('open login window with redirect url: ' + redirect_url);
  const oauthWindow = window.open(
    redirect_url,
    'oauthWindow',
    'width=500,height=800'
  );
  if (oauthWindow == null) {
    console.log('Failed to open OAuth2 login window');
    return;
  }

  //
  // let url = 'https://console.cloud.vmware.com/csp/gateway/discovery?response_type=code&client_id=Gz7vVNL6EkDRuXEE4v5gO8WwfeZ05UuP2dy&redirect_uri=http%3A%2F%2F127.0.0.1%3A31113&state=requested&prompt=login'
  //
  // // Open the OAuth2 login URL in a new window

  // // Check if the OAuth2 process has completed every second
  // const checkInterval = setInterval(() => {
  //     if (oauthWindow.closed) {
  //         clearInterval(checkInterval);
  //
  //         // The window is closed, so the OAuth2 process should be complete. Send the authorization response to the server.
  //         fetch('/oauth_callback')
  //             .then(() => {
  //                 // Handle login completion, e.g. update UI to reflect logged in state
  //             });
  //     }
  // }, 1000);

  // // Get the OAuth2 login URL from the server
  // fetch('/oauth_login_url')
  //     .then(response => response.text())
  //     .then(url => {
  //
  // });
}
