<template>
  <v-container fluid>

  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { IUserProfileUpdate } from "@/interfaces";
import { dispatchGetUsers, dispatchUpdateUser } from "@/store/admin/actions";
import { readAdminOneUser } from "@/store/admin/getters";
import { ValidationProvider, ValidationObserver, extend } from "vee-validate";
import { required, confirmed, email } from "vee-validate/dist/rules";

extend("required", { ...required, message: "{_field_} can not be empty" });
extend("confirmed", { ...confirmed, message: "Passwords do not match" });
extend("email", { ...email, message: "Invalid email address" });

@Component({
  components: {
    ValidationObserver,
    ValidationProvider,
  },
})
export default class EditUser extends Vue {
  $refs!: {
    observer: InstanceType<typeof ValidationObserver>;
  };

  public valid = true;
  public fullName = "";
  public email = "";
  public isActive = true;
  public isSuperuser = false;
  public setPassword = false;
  public password1 = "";
  public password2 = "";

  public async mounted() {
    await dispatchGetUsers(this.$store);
    this.onReset();
  }

  public onReset() {
    this.setPassword = false;
    this.password1 = "";
    this.password2 = "";
    this.$refs.observer.reset();
    if (this.user) {
      this.fullName = this.user.full_name;
      this.email = this.user.email;
      this.isActive = this.user.is_active;
      this.isSuperuser = this.user.is_superuser;
    }
  }

  public cancel() {
    this.$router.back();
  }

  public async onSubmit() {
    const success = await this.$refs.observer.validate();
    if (!success) {
      return;
    }

    const updatedProfile: IUserProfileUpdate = {};
    if (this.fullName) {
      updatedProfile.full_name = this.fullName;
    }
    if (this.email) {
      updatedProfile.email = this.email;
    }
    updatedProfile.is_active = this.isActive;
    updatedProfile.is_superuser = this.isSuperuser;
    if (this.setPassword) {
      updatedProfile.password = this.password1;
    }
    if (this.user) {
      await dispatchUpdateUser(this.$store, {
        id: this.user.id,
        user: updatedProfile,
      });
    }
    this.$router.push("/main/admin/users");
  }

  get user() {
    return readAdminOneUser(this.$store)(+this.$router.currentRoute.params.id);
  }
}
</script>
