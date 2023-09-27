import { OAuthConfig, OAuthUserConfig} from "next-auth/providers";
export interface OidcProfile extends Record<string, any> {
  aud: string
  azp: string
  email: string
  email_verified: boolean
  exp: number
  family_name: string
  given_name: string
  hd: string
  iat: number
  iss: string
  jti: string
  name: string
  nbf: number
  picture: string
  sub: string
}
export default function GigyaProvider<P extends OidcProfile >(
  options: OAuthUserConfig<P>
): OAuthConfig<P> {
  return {
    id: "gigya",
    name: "gigya",
    type: "oauth",
    client: {
      token_endpoint_auth_method: "client_secret_basic"

    },
    authorization: { params: { scope: "openid email profile uid" } },
    profile(profile: P) {

      return {
        id: profile.sub,
        name: profile.name,
        email: profile.email,
        image: profile.picture,
        superAdmin: profile.role === "superAdmin",
        organizations: profile.organizations
      }
    },
    style: {
      logo: "/gigya.svg",
      logoDark: "/gigya-dark.svg",
      bg: "#fff",
      text: "#7289DA",
      bgDark: "#7289DA",
      textDark: "#fff",
    },
    options
  }
}


