package com.dispatchworks.erasure.web;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatus;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.HttpStatusEntryPoint;
import org.springframework.security.web.servlet.util.matcher.PathPatternRequestMatcher;
import org.springframework.security.oauth2.client.registration.ClientRegistration;
import org.springframework.security.oauth2.client.registration.ClientRegistrationRepository;
import org.springframework.security.oauth2.client.registration.InMemoryClientRegistrationRepository;
import org.springframework.security.oauth2.core.AuthorizationGrantType;
import org.springframework.security.oauth2.core.ClientAuthenticationMethod;

@Configuration
class SecurityConfiguration {
    @Bean
    ClientRegistrationRepository employees(
            @Value("${OIDC_ISSUER}") String issuer,
            @Value("${OIDC_BACKCHANNEL_URL}") String backchannel,
            @Value("${OIDC_CLIENT_SECRET}") String secret,
            @Value("${APP_BASE_URL}") String appBaseUrl) {
        // The browser and container have different routes to the same issuer.
        // Keep issuer validation while using explicit internal token/JWK endpoints.
        ClientRegistration registration = ClientRegistration.withRegistrationId("keycloak")
                .clientId("erasure").clientSecret(secret)
                .clientAuthenticationMethod(ClientAuthenticationMethod.CLIENT_SECRET_BASIC)
                .authorizationGrantType(AuthorizationGrantType.AUTHORIZATION_CODE)
                .redirectUri(appBaseUrl + "/login/oauth2/code/keycloak")
                .scope("openid", "profile").issuerUri(issuer)
                .authorizationUri(issuer + "/protocol/openid-connect/auth")
                .tokenUri(backchannel + "/protocol/openid-connect/token")
                .jwkSetUri(backchannel + "/protocol/openid-connect/certs")
                .userInfoUri(backchannel + "/protocol/openid-connect/userinfo")
                .userNameAttributeName("sub").clientName("DispatchWorks").build();
        return new InMemoryClientRegistrationRepository(registration);
    }

    @Bean
    SecurityFilterChain security(HttpSecurity http) throws Exception {
        return http
                .authorizeHttpRequests(auth -> auth
                        .requestMatchers("/", "/index.html", "/assets/**", "/error", "/api/csrf").permitAll()
                        .anyRequest().authenticated())
                .exceptionHandling(errors -> errors.defaultAuthenticationEntryPointFor(
                        new HttpStatusEntryPoint(HttpStatus.UNAUTHORIZED),
                        PathPatternRequestMatcher.withDefaults().matcher("/api/**")))
                .oauth2Login(login -> login.defaultSuccessUrl("/", true))
                .csrf(Customizer.withDefaults())
                .logout(logout -> logout.logoutSuccessHandler((request, response, auth) -> response.setStatus(204)))
                .headers(headers -> headers.contentSecurityPolicy(csp -> csp.policyDirectives(
                        "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; "
                        + "connect-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'")))
                .build();
    }
}
